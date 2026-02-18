from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class ActrConnectionConfig:
    """
    Connection settings for the ACT-R/Phi JSON network interface.

    All values should be provided via the JSON config file.
    """

    hostname: str
    port: int
    sync_mode: Optional[str] = None  # "async", "sync", or "time-locked"


@dataclass
class HumanTraitConfig:
    """
    Psychological and cognitive traits for the virtual human.

    This layer is intentionally generic so you can map it onto
    specific ACT-R/Phi or HumMod parameters in your Lisp code.
    """

    identifier: str
    big_five: Dict[str, float]
    baseline_arousal: float
    fatigue_sensitivity: float
    trust_propensity: float


@dataclass
class EnvironmentConfig:
    """
    High-level environment description (task-agnostic).

    Concrete task parameters live in TaskConfig and are also
    provided only via the JSON config.
    """

    name: str
    description: str
    time_step_seconds: float


@dataclass
class TaskConfig:
    """
    Task-level parameters that will be mirrored on the ACT-R/Phi side.

    Example: Psychomotor Vigilance Task (PVT) settings, reward schemes,
    or any experiment timing parameters.
    """

    name: str
    parameters: Dict[str, Any]


@dataclass
class SimulationConfig:
    """
    Root configuration object for a simulated ACT-R/Phi human.

    This object is purely a structured view of the JSON config.
    """

    actr_connection: ActrConnectionConfig
    human: HumanTraitConfig
    environment: EnvironmentConfig
    task: TaskConfig


class ConfigError(Exception):
    """Raised when the configuration file is missing or malformed."""


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise ConfigError(f"Config file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ConfigError(f"Invalid JSON in config file: {path}") from error


def load_simulation_config(path: str | Path) -> SimulationConfig:
    """
    Load a SimulationConfig instance from a JSON file.

    The file is expected to follow the structure documented in README.md.
    """

    config_path = Path(path)
    raw = _load_json(config_path)

    try:
        conn_raw = raw["actr_connection"]
        human_raw = raw["human"]
        env_raw = raw["environment"]
        task_raw = raw["task"]
    except KeyError as error:
        raise ConfigError(f"Missing top-level key in config: {error}") from error

    connection = ActrConnectionConfig(
        hostname=conn_raw["hostname"],
        port=int(conn_raw["port"]),
        sync_mode=conn_raw.get("sync_mode"),
    )

    human = HumanTraitConfig(
        identifier=human_raw["identifier"],
        big_five=dict(human_raw["big_five"]),
        baseline_arousal=float(human_raw["baseline_arousal"]),
        fatigue_sensitivity=float(human_raw["fatigue_sensitivity"]),
        trust_propensity=float(human_raw["trust_propensity"]),
    )

    environment = EnvironmentConfig(
        name=env_raw["name"],
        description=env_raw["description"],
        time_step_seconds=float(env_raw["time_step_seconds"]),
    )

    task = TaskConfig(
        name=task_raw["name"],
        parameters=dict(task_raw.get("parameters", {})),
    )

    return SimulationConfig(
        actr_connection=connection,
        human=human,
        environment=environment,
        task=task,
    )


class SimulatedActrPhiHuman:
    """
    Minimal Python-side representation of an ACT-R/Phi virtual human.

    Responsibilities:
    - Hold configuration for human traits, environment, and task.
    - Manage a TCP connection to the ACT-R/Phi JSON network interface.
    - Provide simple send/receive methods for JSON messages.

    The actual cognitive model, physiology substrate, and production rules
    remain inside ACT-R/Phi. This class is only the external "agent shell".
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self._socket: Optional[socket.socket] = None

    @classmethod
    def from_config_file(cls, path: str | Path) -> "SimulatedActrPhiHuman":
        """
        Factory that creates a SimulatedActrPhiHuman from a JSON config file.
        """

        simulation_config = load_simulation_config(path)
        return cls(simulation_config)

    def connect(self) -> None:
        """
        Open a TCP connection to the ACT-R/Phi JSON network interface.

        This assumes the Lisp side has already loaded `json-network-interface.lisp`
        and is listening on the configured host and port.
        """

        if self._socket is not None:
            return

        hostname = self.config.actr_connection.hostname
        port = self.config.actr_connection.port

        self._socket = socket.create_connection((hostname, port))
        self._socket.settimeout(5.0)

    def disconnect(self) -> None:
        """
        Close the TCP connection if it is open.
        """

        if self._socket is None:
            return

        try:
            self._socket.close()
        finally:
            self._socket = None

    def send_command(self, method: str, params: Dict[str, Any]) -> None:
        """
        Send a single JSON-RPC-style command to ACT-R/Phi.

        The exact `method` names and `params` structure should mirror the
        JSON API expected by `json-network-interface.lisp` in the ACT-R/Phi
        code base (e.g., `display-new`, `keypress`, `trigger-reward`, etc.).
        """

        if self._socket is None:
            raise RuntimeError("Connection not open. Call connect() first.")

        payload = {
            "model": self.config.human.identifier,
            "method": method,
            "params": params,
        }
        message = json.dumps(payload)
        data = (message + "\r\n").encode("utf-8")
        self._socket.sendall(data)

    def receive_event(self) -> Optional[Dict[str, Any]]:
        """
        Read a single JSON event from ACT-R/Phi if available.

        Returns None on timeout. The caller can poll this method
        between environment updates to process cognitive events.
        """

        if self._socket is None:
            raise RuntimeError("Connection not open. Call connect() first.")

        try:
            raw = self._socket.recv(4096)
        except socket.timeout:
            return None

        if not raw:
            return None

        try:
            text = raw.decode("utf-8").strip()
            if not text:
                return None
            return json.loads(text)
        except json.JSONDecodeError:
            # The upstream protocol can be extended later;
            # for now we fail silently to keep the shell lightweight.
            return None


def demo_from_config(config_path: str | Path) -> None:
    """
    Small demonstration function used in the README.

    It loads a config, connects to ACT-R/Phi, and sends a placeholder
    `setup` command with environment and task metadata.
    """

    human = SimulatedActrPhiHuman.from_config_file(config_path)
    human.connect()

    setup_payload: Dict[str, Any] = {
        "human_traits": {
            "identifier": human.config.human.identifier,
            "big_five": human.config.human.big_five,
            "baseline_arousal": human.config.human.baseline_arousal,
            "fatigue_sensitivity": human.config.human.fatigue_sensitivity,
            "trust_propensity": human.config.human.trust_propensity,
        },
        "environment": {
            "name": human.config.environment.name,
            "description": human.config.environment.description,
            "time_step_seconds": human.config.environment.time_step_seconds,
        },
        "task": {
            "name": human.config.task.name,
            "parameters": human.config.task.parameters,
        },
    }

    human.send_command(method="setup-virtual-human", params=setup_payload)

