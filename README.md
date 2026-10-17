
Architect:Chutiphong Bunloed (Buriram, Thailand)

Orcid:0009-0003-4295-7521
DOI 10.5281/Zenodo.23286311

# AQEH32: Hybrid Quantum Error Correction & Passive Healing Simulator

**AQEH32** is a Python framework designed to simulate a **Hybrid Quantum Error Correction (QEC)** architecture for **5-level quantum systems (qudits)** on a multi-site network. The platform bridges the gap between digital software-driven error detection and physical hardware-driven automated healing.

---

## 🚀 Key Benefits & Value Propositions

* **Minimized Performance Overhead:** By allowing continuous passive healing to catch minor errors automatically, the system reduces the need to run heavy digital decoding software constantly. This minimizes the risk of introducing additional noise during active inspection.
* **Leakage and Phase Protection:** The dual-filter decoding system is explicitly optimized for high-dimensional 5-level systems, providing strong defense lines against state leakages and multi-level phase errors.
* **Resonance Avoidance via Smart Timing:** Instead of checking for errors at constant, predictable intervals, the simulator uses a non-periodic Fibonacci clock sequence. This prevents the system from locking gears with outside periodic noise, preventing data corruption.

---

## 🛠️ How it Works & Architecture

The simulator coordinates the protection task across different logical layers:
* **The Foundation & Encoding Layers:** Setup the physical rules, coordinate mappings, and structural symmetry of the 5-level network to keep the logical workspace secure.
* **The Timing Layer:** Operates as a smart clock that determines the exact, non-linear moments when the system should actively step in to check for faults.
* **The Active Decoder Layer:** Executes a step-by-step algorithm to intercept, evaluate, and filter out fake error signals, choosing the most likely physical error to correct.
* **The Passive Healing Layer:** Simulates a natural environmental dampening effect that automatically pushes stray particles and corrupted states back into their proper original slots without software intervention.

---

## 💻 Usage & Quick Start

### Prerequisites
* Python 3.8+
* NumPy
* SciPy

### Basic Simulation Workflow
You can run a complete hybrid simulation loop by setting up the passive decay time frame, letting the system run, and calling the decoder to fix unresolved errors:

```python
import numpy as np

# 1. Setup the system dimensions and the simulation timeline
dim = total_dim()
times = np.linspace(0, 10, 100)

# 2. Initialize your initial system state and the automated passive healing layer
rho_init = np.zeros((dim, dim), dtype=complex)
rho_init[0, 0] = 1.0  # Start from a clean baseline state
L_heal = build_L_heal()

# 3. Step A: Let the system evolve through continuous passive healing
simulated_states = evolve(rho_init, L_heal, times)

# 4. Step B: Trigger the Active Decoder to identify residual errors
decoder = Decoder()
all_candidates = decoder.step3_generate_candidates(max_weight=2)

# Provide a sample error syndrome reading captured by the system
syndrome_sample = (1, 4) 
detected_error = decoder.decode(syndrome_sample, all_candidates)

# 5. Step C: Apply the structural correction to restore the system
latest_state = simulated_states[-1]
restored_state = apply_correction(latest_state, detected_error)
```

---

## 🤝 Contributing

* Testing the code against different types of random noise environments.
* Optimizing the active decoder script to support a higher number of network sites.
* Writing data visualization tools to graph the system's survival rate over time.

Copyright (c) 2026 Chutiphong Bunloed   All Rights Reserved.
