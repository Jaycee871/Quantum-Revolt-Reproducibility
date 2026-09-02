#!/usr/bin/env python3
"""Guarded CHSH experiment for IBM Quantum hardware.

This script does not submit a QPU job unless the caller explicitly passes
--confirm-hardware-run. The reproducer must provide their own IBM Quantum
credential through the IBM_QUANTUM_API environment variable.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


def build_circuit(alpha: float, beta: float) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-2 * alpha, 0)
    qc.ry(-2 * beta, 1)
    qc.measure_all()
    return qc


def correlation(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total == 0:
        raise ValueError("No measurement counts returned")
    same = counts.get("00", 0) + counts.get("11", 0)
    diff = counts.get("01", 0) + counts.get("10", 0)
    return (same - diff) / total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--shots", type=int, default=512)
    parser.add_argument("--optimization-level", type=int, default=1, choices=[0, 1, 2, 3])
    parser.add_argument("--output", default="results/reproduced_ibm_chsh_hardware.json")
    parser.add_argument(
        "--confirm-hardware-run",
        action="store_true",
        help="Required safety lock: acknowledge that this submits a real QPU job and may consume plan quota.",
    )
    args = parser.parse_args()

    if not args.confirm_hardware_run:
        raise SystemExit(
            "Hardware submission locked. Re-run with --confirm-hardware-run only after explicit quota/cost approval."
        )

    token = os.environ.get("IBM_QUANTUM_API")
    if not token:
        raise SystemExit("IBM_QUANTUM_API is not set")
    if args.shots < 1 or args.shots > 4096:
        raise SystemExit("--shots must be between 1 and 4096")

    service = QiskitRuntimeService(token=token)
    backend = service.backend(args.backend)
    status = backend.status()
    if not status.operational:
        raise SystemExit(f"Backend {args.backend} is not operational: {status.status_msg}")

    settings = {
        "A0B0": (0.0, math.pi / 8),
        "A0B1": (0.0, -math.pi / 8),
        "A1B0": (math.pi / 4, math.pi / 8),
        "A1B1": (math.pi / 4, -math.pi / 8),
    }

    circuits = [build_circuit(*settings[label]) for label in settings]
    pass_manager = generate_preset_pass_manager(
        backend=backend, optimization_level=args.optimization_level
    )
    isa_circuits = pass_manager.run(circuits)

    circuit_metadata = []
    for label, circuit in zip(settings, isa_circuits):
        ops = {str(k): int(v) for k, v in circuit.count_ops().items()}
        two_qubit_ops = sum(v for k, v in ops.items() if k in {"cx", "cz", "ecr"})
        circuit_metadata.append(
            {
                "label": label,
                "depth": int(circuit.depth()),
                "size": int(circuit.size()),
                "two_qubit_gate_count": int(two_qubit_ops),
                "operations": ops,
                "layout": repr(circuit.layout),
            }
        )

    sampler = Sampler(mode=backend)
    job = sampler.run(isa_circuits, shots=args.shots)
    job_id = job.job_id()
    result = job.result()

    measured = {}
    for label, pub_result in zip(settings, result):
        counts = pub_result.data.meas.get_counts()
        counts = {str(k): int(v) for k, v in counts.items()}
        measured[label] = {
            "counts": counts,
            "correlation": correlation(counts),
        }

    S = (
        measured["A0B0"]["correlation"]
        + measured["A0B1"]["correlation"]
        + measured["A1B0"]["correlation"]
        - measured["A1B1"]["correlation"]
    )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "IBM Quantum",
        "backend": backend.name,
        "backend_num_qubits": backend.num_qubits,
        "pending_jobs_at_submission": getattr(status, "pending_jobs", None),
        "status_message_at_submission": getattr(status, "status_msg", None),
        "runtime_job_id": job_id,
        "shots_per_setting": args.shots,
        "optimization_level": args.optimization_level,
        "state": "|Phi+>",
        "classical_chsh_bound": 2.0,
        "tsirelson_bound": 2 * math.sqrt(2),
        "S": S,
        "absolute_S": abs(S),
        "violates_classical_bound": abs(S) > 2.0,
        "measurement_results": measured,
        "transpiled_circuits": circuit_metadata,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"IBM Quantum job: {job_id}")
    print(f"Backend: {backend.name}")
    print(f"CHSH S = {S:.6f}; |S| = {abs(S):.6f}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
