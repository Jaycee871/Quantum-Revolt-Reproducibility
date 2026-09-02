#!/usr/bin/env python3
"""Finite-shot CHSH simulator used for the Quantum Revolt reproducibility package."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_circuit(alpha: float, beta: float) -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-2 * alpha, 0)
    qc.ry(-2 * beta, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def correlation(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    same = counts.get("00", 0) + counts.get("11", 0)
    diff = counts.get("01", 0) + counts.get("10", 0)
    return (same - diff) / total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=8192)
    parser.add_argument("--output", default="results/reproduced_chsh_simulation.json")
    args = parser.parse_args()

    backend = AerSimulator()
    settings = {
        "A0B0": (0.0, math.pi / 8),
        "A0B1": (0.0, -math.pi / 8),
        "A1B0": (math.pi / 4, math.pi / 8),
        "A1B1": (math.pi / 4, -math.pi / 8),
    }

    results = {}
    for label, (alpha, beta) in settings.items():
        circuit = transpile(build_circuit(alpha, beta), backend)
        counts = backend.run(circuit, shots=args.shots).result().get_counts()
        results[label] = {
            "alpha_rad": alpha,
            "beta_rad": beta,
            "counts": {str(k): int(v) for k, v in counts.items()},
            "correlation": correlation(counts),
        }

    S = (
        results["A0B0"]["correlation"]
        + results["A0B1"]["correlation"]
        + results["A1B0"]["correlation"]
        - results["A1B1"]["correlation"]
    )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "backend": "AerSimulator",
        "state": "|Phi+>",
        "shots_per_setting": args.shots,
        "classical_chsh_bound": 2.0,
        "tsirelson_bound": 2 * math.sqrt(2),
        "S": S,
        "absolute_S": abs(S),
        "violates_classical_bound": abs(S) > 2.0,
        "settings": results,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"CHSH S = {S:.6f}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
