### Simulated ACT-R/Phi Human

This folder contains a **minimal Python shell** around the ACT-R/Phi code in `Modeling/act-r_phi`.  
The goal is to configure a *virtual human* in one place (a JSON file) and talk to the ACT-R/Phi model over the existing JSON network interface.

- **No human / environment / task numbers are hard-coded in the Python code.**
- **All individual-, environment-, and task-specific values live in a JSON config file.**

The actual **cognitive architecture**, **physiology substrate (HumMod)**, and **task logic** still live in the Lisp side (ACT-R/Phi).

---

### 1. Files in this folder

- `human.py`  
  Python-side representation of a simulated ACT-R/Phi human:
  - Loads a structured config (`SimulationConfig`).
  - Manages a TCP socket to the ACT-R/Phi JSON network interface (`json-network-interface.lisp`).
  - Sends and receives JSON messages (methods and params match whatever you implement on the Lisp side).

- `config.example.json`  
  Example configuration file. Copy and edit this instead of touching the Python code when you change:
  - Human traits (Big Five, arousal, fatigue, trust).
  - Environment timing.
  - Task parameters (e.g., PVT session length, thresholds).
  - Connection host/port and sync mode.

- `README.md` (this file)  
  Short tutorial for setting up, running, and interacting with the virtual human.

You can also create your own `config.json` next to these files and point the code to it.

---

### 2. Config structure (one place for all knobs)

The configuration is a single JSON object with four main sections:

- **`actr_connection`**: how Python talks to ACT-R/Phi.
- **`human`**: psychological and cognitive traits for the virtual subject.
- **`environment`**: high-level description and timing of the lab/task world.
- **`task`**: task-specific parameters that should mirror the ACT-R/Phi model settings.

Example (shortened) config:

```json
{
  "actr_connection": {
    "hostname": "localhost",
    "port": 5555,
    "sync_mode": "async"
  },
  "human": {
    "identifier": "virtual_subject_01",
    "big_five": {
      "agreeableness": 0.6,
      "openness": 0.7,
      "conscientiousness": 0.5,
      "extraversion": 0.4,
      "neuroticism": 0.3
    },
    "baseline_arousal": 0.5,
    "fatigue_sensitivity": 0.8,
    "trust_propensity": 0.6
  },
  "environment": {
    "name": "PVT_lab",
    "description": "Psychomotor Vigilance Task environment with ACT-R/Phi physiology enabled.",
    "time_step_seconds": 0.5
  },
  "task": {
    "name": "PVT",
    "parameters": {
      "session_length_minutes": 10
    }
  }
}
```

You control **all individual differences and task/environment setups** by editing this JSON, not the code.

---

### 3. How the Python side is structured

- **`SimulationConfig`** (in `human.py`):
  - Wraps four lower-level configs:
    - `ActrConnectionConfig`
    - `HumanTraitConfig`
    - `EnvironmentConfig`
    - `TaskConfig`
  - Created by `load_simulation_config(path)`.

- **`SimulatedActrPhiHuman`**:
  - Holds a `SimulationConfig`.
  - Opens a TCP socket to ACT-R/Phi (`connect()` / `disconnect()`).
  - Sends JSON commands with `send_command(method, params)`.
  - Optionally reads back events with `receive_event()`.

The **ACT-R/Phi side** is still responsible for:

- Loading the architecture (`load-act-r.lisp`).
- Loading your physiology module (`Physiology_thread` and related files).
- Loading your cognitive model (e.g., PVT model in `test-model.lisp`).
- Loading and configuring `json-network-interface.lisp`.

---

### 4. Step-by-step: set up and run the human

#### 4.1. Prepare ACT-R/Phi (Lisp side)

1. **Start your Lisp environment** (e.g., SBCL, CCL) and change directory to `Modeling/act-r_phi`.
2. **Load ACT-R**:
   - Run `(load "load-act-r.lisp")`.
3. **Load your ACT-R/Phi model and physiology substrate**:
   - Load `Physiology_thread` (or the modern physiology module you use).
   - Load your cognitive model (for example, the PVT model in `test-model.lisp`).
4. **Load the JSON network interface**:
   - `(load "json-network-interface.lisp")`
   - In your model, create and configure the module using the parameters it defines:
     - `:jni-hostname` (must match `actr_connection.hostname` in JSON).
     - `:jni-port` (must match `actr_connection.port`).
     - `:jni-sync` (corresponds conceptually to `sync_mode`).
5. **Start the environment server** on the Lisp side:
   - Use your existing ACT-R/Phi infrastructure (or extend it) so that:
     - ACT-R opens a TCP server on the configured host/port.
     - It uses the JSON protocol from `json-network-interface.lisp`.

At this point the **Lisp process is the “brain + body”**, and you can either:

- Let **Python act as the environment server** (ACT-R/Phi connects to Python).
- Or let **Python act as a client** (connects to an ACT-R/Phi JSON server).

---

#### 4.2. Option A: Python as environment server (ACT-R/Phi connects)

This matches how `json-network-interface.lisp` is commonly used (ACT-R as TCP client).

1. Go to `Models/simulated actrphi human/`.
2. **Copy the example config** (if needed):

   ```bash
   cp "config.example.json" "config.json"
   ```

3. Edit `config.json`:
   - **Connection**:
     - Set `"hostname"` and `"port"` to where you want Python to listen (e.g. `"localhost"` and `5555`).
   - **Human traits / environment / task**:
     - Configure these as described in section 2.

4. **Start the Python environment server**:

   ```bash
   cd "<repo-root>/Models/simulated actrphi human"
   python3 server.py config.json
   ```

   You should see:

   ```text
   [server] Listening on localhost:5555
   [server] Human 'virtual_subject_01' in env 'PVT_lab' (task: PVT)
   ```

5. **Point ACT-R/Phi at this server**:

   ```lisp
   (load "json-network-interface.lisp")

   (sgp :json-network-interface
        (list :jni-hostname "localhost"
              :jni-port 5555
              :jni-sync nil))
   ```

   When your ACT-R/Phi model uses the JSON interface, messages will appear in the Python server log.  
   The default `ActrEnvironmentServer` implementation:

   - Logs each message (`model`, `method`, `params`).
   - Sends back a simple JSON acknowledgement.

   You can extend `ActrEnvironmentServer.handle_message` in `server.py` to interpret specific methods and update a richer environment.

---

#### 4.3. Option B: Python as client (connects to ACT-R/Phi)

In this case ACT-R/Phi exposes a JSON server and Python connects using `SimulatedActrPhiHuman`.

1. Go to `Models/simulated actrphi human/`.
2. **Copy the example config**:

   ```bash
   cp "config.example.json" "config.json"
   ```

3. Edit `config.json`:
   - **Connection**:
     - Set `"hostname"` and `"port"` to match the ACT-R/Phi JSON server.
     - Choose `"sync_mode"` to match how you configured `:jni-sync` on the Lisp side.
   - **Human traits**:
     - Choose an `"identifier"` (this can be used as ACT-R model name if you want).
     - Set the Big Five scores and other trait-like parameters as floats in \[0, 1\] (or any scale you prefer).
   - **Environment**:
     - Give the environment a descriptive `"name"` and `"description"`.
     - Set `"time_step_seconds"` to the integration step you want for stepping the environment.
   - **Task**:
     - Set `"name"` to the task label you use in your Lisp code (e.g., `"PVT"`).
     - Add any additional `"parameters"` your model expects (e.g., thresholds, durations).

You do **not** need to change `human.py` when you change any of these values.

---

#### 4.4. Run a minimal test from Python

You can use the small demo function in `human.py`:

```bash
cd "<repo-root>/Models/simulated actrphi human"
python -c "from human import demo_from_config; demo_from_config('config.json')"
```

This does the following:

- Loads `config.json` into a `SimulationConfig`.
- Creates a `SimulatedActrPhiHuman`.
- Connects to ACT-R/Phi over TCP.
- Sends a `setup-virtual-human` command with:
  - Human traits.
  - Environment description.
  - Task name and parameters.

On the **Lisp side**, you would handle this method in your JSON environment dispatcher, for example:

- When you see method `"setup-virtual-human"`:
  - Create or configure an ACT-R model for that subject.
  - Set physiological variables, fatigue parameters, or utility parameters based on the payload.
  - Initialize task state (e.g., schedule the first PVT trial).

---

### 5. Interacting with the human

The key operations from Python are:

- **Send inputs**:

  ```python
  from pathlib import Path
  from human import SimulatedActrPhiHuman

  h = SimulatedActrPhiHuman.from_config_file(Path("config.json"))
  h.connect()

  # Example: present a new stimulus in the environment
  h.send_command(
      method="display-new",
      params={
          "stimulus": {
              "type": "pvt-target",
              "onset_time": 123.45,
              "location": [100, 100]
          }
      },
  )
  ```

  The exact `method` and `params` structure must match what you implement in your ACT-R/Phi JSON handler (likely reusing or extending the existing `display-new` / `update-display` code).

- **Receive outputs**:

  ```python
  event = h.receive_event()
  if event is not None:
      # Example: log model response or update your environment state
      print("ACT-R/Phi event:", event)
  ```

Typical events might include:

- Model keypresses / button presses.
- Decisions or responses (e.g., “respond” in PVT).
- Internal events you choose to serialize as JSON (e.g., arousal, utility values, DM state summaries).

---

### 6. Changing environment and human traits

To **change the environment**:

- Edit the `"environment"` block in your JSON:
  - Change `"name"` and `"description"`.
  - Change `"time_step_seconds"` if you want a finer or coarser interaction loop.
  - Add more environment-specific keys into `task.parameters` if they are per-task.

To **change human traits**:

- Edit the `"human"` block:
  - Update `"big_five"` scores.
  - Adjust `"baseline_arousal"`, `"fatigue_sensitivity"`, and `"trust_propensity"`.
  - Use `"identifier"` to differentiate multiple virtual subjects.

On the **Lisp side**, you should:

- Map these fields into:
  - ACT-R parameters (e.g., `:dat`, `:ans`, `:iu`, utility scalars).
  - Physiology parameters (e.g., recorded variables in `Physiology_thread`, homeostatic settings, daily planner schedule).
  - Task parameters (e.g., `threshScalar`, `noiseScalar`, durations).

That mapping is model-specific, but the important part is that all the **inputs come from the JSON**, not the Python code.

---

### 7. Recommended workflow

- **1. Design the ACT-R/Phi model** in Lisp (cognition + physiology + task).
- **2. Decide what should be configurable per human / environment / task.**
- **3. Add those fields to your JSON config** under `human`, `environment`, or `task`.
- **4. Extend your Lisp JSON handler** so that:
  - It reads those fields and maps them to ACT-R parameters, physio variables, or task settings.
- **5. Use the Python `SimulatedActrPhiHuman`** to:
  - Send a single `setup-virtual-human` message at the start.
  - Then send per-step environment updates and read back events.

This keeps:

- **All knobs** in one JSON file.
- **Minimal, clean Python code**.
- **Most complexity** on the ACT-R/Phi side, where the architecture already lives.

