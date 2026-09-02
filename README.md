# Quantum Revolt — Reproducibility Package

Public reproducibility materials for the preprint **Quantum Revolt: Nietzsche, Camus, Kuhn, and the Limits of Scientific Intelligibility** by Pack Kwan Low.

## Purpose

This repository is a deliberately minimal public data and reproducibility snapshot for OSF / MetaArXiv and related preprint records. It is separate from the manuscript-development repository so that submission metadata, reviewer notes, GitHub credential tests, and internal research materials are not mixed with the public reproducibility record.

## What is reproduced here

The manuscript uses a small CHSH operational case study to distinguish software-level execution from real-device material execution. The case study is **methodological**: it is not presented as a new Bell experiment, a loophole-free Bell test, or novel evidence for nonlocality.

| Run | Backend | Shots per setting | CHSH S |
|---|---|---:|---:|
| Simulator | Qiskit AerSimulator | 8192 | 2.805419921875 |
| Hardware | IBM Quantum `ibm_marrakesh` | 512 | 2.6796875 |

The classical CHSH bound is 2. The Tsirelson bound is approximately 2.828427.

## Repository contents

- `results/phase1_chsh_simulation.json` — frozen finite-shot simulator output.
- `results/phase2_ibm_chsh_hardware_summary.json` — frozen real-QPU output and transpilation summary.
- `experiments/chsh_simulator.py` — standalone simulator reproduction script reconstructed from the original Phase-1 workflow.
- `experiments/ibm_chsh_hardware.py` — guarded IBM Quantum hardware script. It will not submit a QPU job without explicit `--confirm-hardware-run` acknowledgement.
- `REPRODUCIBILITY.md` — reproduction instructions, scope, and limitations.
- `PROVENANCE.md` — provenance of the frozen records and links to the manuscript-development repository.
- `requirements.txt` — required Python packages. Exact package versions were not frozen in the original run; this limitation is documented.

## Data availability statement

All data used for the repository-level CHSH operational case study are publicly available in this repository. The frozen JSON files contain the simulator and IBM Quantum hardware results used in the manuscript.

## Security and privacy

This repository contains **no API keys, tokens, `.env` files, GitHub credential-test workflows, arXiv account metadata, reviewer notes, or private submission materials**. Real-QPU reproduction requires the reproducer to provide their own IBM Quantum credential through an environment variable.

## Related manuscript repository

Development repository: `Jaycee871/Beyond-the-Paradigm-Nietzsche-Camus-and-the-Philosophy-of-Intellectual-Revolt`

## Citation

Please cite the associated preprint once its persistent identifier is available. Until then, cite this repository as the reproducibility package for *Quantum Revolt* by Pack Kwan Low.
