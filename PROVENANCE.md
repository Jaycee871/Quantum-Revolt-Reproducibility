# Provenance

## Associated manuscript

**Title:** *Quantum Revolt: Nietzsche, Camus, Kuhn, and the Limits of Scientific Intelligibility*  
**Author:** Pack Kwan Low  
**Affiliation:** Department of Information Management, Chinese Culture University, Taiwan

Manuscript-development repository:

`Jaycee871/Beyond-the-Paradigm-Nietzsche-Camus-and-the-Philosophy-of-Intellectual-Revolt`

Snapshot reference for the manuscript repository at the time this public reproducibility package was assembled:

`01dc742930f5089b80d9833622c86ca81ceb2d38`

## Simulator record

Original source path:

`results/phase1_chsh_simulation.json`

Original Git blob SHA:

`a15cbfc317a805bde79d73d232fe61bb8d7b0916`

Generated:

`2026-09-02T17:23:36.893795+00:00`

Key result:

`S = 2.805419921875` with 8192 shots per setting on Qiskit `AerSimulator`.

## IBM Quantum hardware record

Original source path:

`results/phase2_ibm_chsh_hardware_summary.json`

Original Git blob SHA:

`674d6082184f989de6af2a9bcafdf874353be884`

Generated:

`2026-09-02T17:57:17.757057+00:00`

Provider / backend:

`IBM Quantum / ibm_marrakesh`

Runtime job identifier:

`dac66td1ierc738j6srg`

Key result:

`S = 2.6796875` with 512 shots per setting, optimization level 1, and no error mitigation.

Original GitHub Actions execution record embedded in the frozen result:

- workflow run ID: `33664179371`
- artifact ID: `9859892702`
- artifact SHA-256: `20d895dfdd600dffa84729e97233c038136d773223df84fc577c0999ddb7edc1`

## Hardware script provenance

Original source path:

`experiments/ibm_chsh_hardware.py`

Original Git blob SHA:

`ba21684d9068e75cd10f77d8e36c73fc536e195c`

The copy in this repository preserves the experiment logic and safety lock while clarifying that reproducers must supply their own IBM Quantum credential.

## Simulator script provenance

The original simulator implementation was embedded in `.github/workflows/quantum-revolt-phase1.yml` rather than stored as a standalone Python file. The standalone `experiments/chsh_simulator.py` in this repository is a direct extraction/reconstruction of that implementation for public reproducibility.

Original workflow Git blob SHA:

`0169ffcf6e354b85c798f5412c32f26748f4515a`

## Scope

These records support only the manuscript's repository-level operational case study. They do not constitute a new foundational-physics dataset or a loophole-free Bell-test record.
