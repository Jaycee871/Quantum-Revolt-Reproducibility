# Data Dictionary

This document describes the two frozen JSON records in `results/`.

## Common CHSH fields

| Field | Meaning |
|---|---|
| `generated_at_utc` | UTC timestamp when the record was generated. |
| `state` | Prepared Bell state, here `|Phi+>`. |
| `shots_per_setting` | Number of measurement shots for each of the four CHSH settings. |
| `classical_chsh_bound` | Classical-local CHSH bound, 2. |
| `tsirelson_bound` | Quantum upper bound for CHSH, `2*sqrt(2)`. |
| `S` | Signed CHSH statistic computed from the four correlations. |
| `absolute_S` | Absolute value of the CHSH statistic. |
| `violates_classical_bound` | Whether `|S| > 2` for the frozen run. |

## Simulator record

File: `results/phase1_chsh_simulation.json`

Each entry under `settings` contains:

| Field | Meaning |
|---|---|
| `alpha_rad` | Measurement-axis angle for qubit A in radians. |
| `beta_rad` | Measurement-axis angle for qubit B in radians. |
| `counts` | Observed finite-shot bitstring counts. |
| `correlation` | `(N_same - N_different) / N_total`. |

## Hardware record

File: `results/phase2_ibm_chsh_hardware_summary.json`

Additional fields include:

| Field | Meaning |
|---|---|
| `provider` | Quantum-computing service used for the run. |
| `backend` | IBM Quantum backend selected for execution. |
| `backend_num_qubits` | Backend qubit count reported at execution time. |
| `pending_jobs_at_submission` | Queue count observed when the job was submitted. |
| `runtime_job_id` | Opaque IBM Runtime job identifier retained for provenance; it is not an authentication credential. |
| `optimization_level` | Qiskit transpilation optimization level. |
| `measurement_results` | Counts and correlations from the four hardware measurement settings. |
| `transpilation_summary` | Compact metadata about mapped qubits, circuit depth, size, and native two-qubit gate count. |
| `approx_independent_shot_standard_error_S` | Simple independent-shot approximation to the standard error of `S`; not a full device-noise model. |
| `reproducibility` | GitHub Actions provenance for the frozen original run. |
| `interpretive_scope` | Explicit limitation on what the hardware run is claimed to establish. |

## Interpretation warning

The hardware JSON is a reproducibility record for a repository-level operational case study. It is not a loophole-free Bell-test dataset and should not be interpreted as a new foundational-physics result.
