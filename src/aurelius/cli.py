"""Command-line interface for repeatable synthetic experiments."""

from __future__ import annotations

import argparse
import json

from .benchmark import run_benchmark


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aurelius",
        description="Run reproducible synthetic audio algorithm experiments (not a hearing device).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    bench = sub.add_parser("benchmark", help="run the synthetic profile/noise benchmark")
    bench.add_argument("--output", default="results/synthetic-v0.2", help="output directory")
    bench.add_argument("--seed", type=int, default=20261124)
    bench.add_argument("--trials-per-condition", type=int, default=3)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "benchmark":
        summary = run_benchmark(args.output, seed=args.seed, trials_per_condition=args.trials_per_condition)
        print(json.dumps({k: summary[k] for k in ("benchmark", "n_trials", "n_rows", "scope_warning")}, indent=2))
        print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
