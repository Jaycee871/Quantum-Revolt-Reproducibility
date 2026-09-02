# Reproducibility Guide

## Scope

This package reproduces the repository-level CHSH operational case study used in *Quantum Revolt: Nietzsche, Camus, Kuhn, and the Limits of Scientific Intelligibility*.

The case study has two parts:

1. a finite-shot simulator baseline;
2. a real IBM Quantum hardware execution.

The purpose is methodological. It demonstrates the difference between software-level execution and execution under real-device constraints. It is not offered as a novel Bell test, a loophole-free Bell experiment, or new evidence for quantum nonlocality.

## Frozen reference results

The exact records cited by the manuscript are preserved in:

- `results/phase1_chsh_simulation.json`
- `results/phase2_ibm_chsh_hardware_summary.json`

Reference values:

- Simulator: `S = 2.805419921875`, 8192 shots per setting.
- IBM Quantum hardware: `S = 2.6796875`, 512 shots per setting, backend `ibm_marrakesh`, no error mitigation.

Because both experiments use finite sampling, a new run is not expected to reproduce the final decimal digits exactly.

## Installation

Create an isolated Python environment if possible, then install:

```bash
python -m pip install -r requirements.txt
```

### Environment limitation

The original GitHub Actions runs installed the then-current Qiskit packages on 2026-09-02 without an exact version lockfile. Exact package versions were therefore not captured in the original execution record. `requirements.txt` records the required packages, not a claim of byte-for-byte environment reconstruction.

## Reproduce the simulator case

```bash
python experiments/chsh_simulator.py --shots 8192
```

By default the new output is written to:

```text
results/reproduced_chsh_simulation.json
```

The expected qualitative result is a finite-shot value close to the Tsirelson-optimal CHSH value and above the classical bound of 2.

## Reproduce the IBM Quantum case

### 1. Use your own credential

Set an IBM Quantum API credential in your local environment. Do not commit it to this repository.

Example shell convention:

```bash
export IBM_QUANTUM_API='YOUR_OWN_TOKEN'
```

### 2. Check backend availability

The original run used `ibm_marrakesh`. IBM backend availability, calibration, queue length, topology, and service plans can change. If that backend is unavailable to your account, choose an accessible operational backend and record the substitution.

### 3. Explicitly unlock hardware submission

The hardware script contains a safety lock. Without `--confirm-hardware-run`, it exits before submitting a QPU job.

```bash
python experiments/ibm_chsh_hardware.py \
  --backend ibm_marrakesh \
  --shots 512 \
  --optimization-level 1 \
  --confirm-hardware-run
```

A hardware reproduction can consume account quota and can produce a different numerical value because of device noise, calibration state, transpilation, finite sampling, and backend changes.

## Interpretation of differences

A successful reproduction does not require the hardware value to equal `2.6796875`. The philosophical point does not depend on one exact number. The frozen run documents that the same formal CHSH structure can be compiled and executed through a real quantum-computing stack while remaining exposed to material conditions absent from an idealized software model.

## Security

- No credential is stored in this repository.
- Do not commit `.env` files or API tokens.
- The IBM script requires an explicit hardware-run acknowledgement.
- No GitHub Actions workflow in this public package is configured to consume repository secrets.

## Data integrity

Treat the two files under `results/` as frozen reference records. New reproductions should be saved under new filenames rather than overwriting the frozen files.
