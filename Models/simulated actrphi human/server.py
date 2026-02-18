from __future__ import annotations

import json
import socket
from pathlib import Path
from typing import Any, Dict, Optional, TextIO

from human import SimulationConfig, load_simulation_config


class ActrEnvironmentServer:
    """
    Minimal TCP JSON server for ACT-R/Phi.

    Responsibilities:
    - Listen on the host/port specified in the JSON config.
    - Accept a single ACT-R/Phi client connection at a time.
    - Read line-delimited JSON messages from ACT-R/Phi.
    - Log messages and send simple JSON acknowledgements.

    This server is intentionally lightweight. You can extend
    the `handle_message` method to:
      - Update a richer Python-side environment state.
      - Drive other simulators (e.g., robot simulators).
      - Log and analyze ACT-R/Phi outputs.
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self._server_socket: Optional[socket.socket] = None

    @property
    def host(self) -> str:
        return self.config.actr_connection.hostname

    @property
    def port(self) -> int:
        return self.config.actr_connection.port

    def start(self) -> None:
        """
        Start the TCP server and block, serving connections sequentially.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            print(f"[server] Listening on {self.host}:{self.port}")
            print(
                f"[server] Human '{self.config.human.identifier}' in env "
                f"'{self.config.environment.name}' (task: {self.config.task.name})"
            )

            while True:
                client_socket, address = server_socket.accept()
                try:
                    print(f"[server] Accepted connection from {address}")
                    self._serve_client(client_socket)
                finally:
                    try:
                        client_socket.close()
                    except OSError:
                        pass

    def _serve_client(self, client_socket: socket.socket) -> None:
        """
        Handle a single client connection until it closes.
        """

        file_obj: TextIO = client_socket.makefile("rwb")

        for raw_line in file_obj:
            try:
                text = raw_line.decode("utf-8").strip()
            except UnicodeDecodeError:
                print("[server] Received non-UTF8 data; ignoring line.")
                continue

            if not text:
                continue

            try:
                message = json.loads(text)
            except json.JSONDecodeError:
                print(f"[server] Invalid JSON from client: {text!r}")
                continue

            response = self.handle_message(message)

            if response is not None:
                serialized = json.dumps(response) + "\r\n"
                file_obj.write(serialized.encode("utf-8"))
                file_obj.flush()

    def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single JSON message from ACT-R/Phi.

        Default behavior:
        - Log the message.
        - Echo a simple acknowledgement with the same `method`.

        You can extend this to:
        - Interpret `method` names such as 'display-new', 'keypress',
          'trigger-reward', or your own custom methods.
        - Update Python-side state representing the environment
          and the virtual human.
        """

        model = message.get("model")
        method = message.get("method")
        params = message.get("params")

        print(f"[server] message from model={model!r}, method={method!r}")
        print(f"[server] params: {json.dumps(params, indent=2)}")

        return {
            "status": "ok",
            "echo_method": method,
        }


def run_server(config_path: str | Path) -> None:
    """
    Load the simulation config and run the ACT-R/Phi environment server.
    """

    simulation_config = load_simulation_config(config_path)
    server = ActrEnvironmentServer(simulation_config)

    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[server] Shutting down on KeyboardInterrupt.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the ACT-R/Phi environment server using a JSON config."
    )
    parser.add_argument(
        "config",
        type=str,
        help="Path to the JSON config file (e.g., config.json).",
    )

    args = parser.parse_args()
    run_server(args.config)

