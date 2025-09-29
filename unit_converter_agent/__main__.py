"""Command line entry point for the unit converter agent."""
from __future__ import annotations

import argparse
import json
from typing import Any

from . import UnitConverterAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit conversion helper")
    parser.add_argument("value", type=float, help="Numeric value to convert")
    parser.add_argument("src_unit", help="Source unit, e.g. 'km'")
    parser.add_argument("tgt_unit", help="Target unit, e.g. 'm'")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the result as a JSON object (value + metadata)",
    )
    return parser


def main(argv: list[str] | None = None) -> Any:
    parser = build_parser()
    args = parser.parse_args(argv)

    agent = UnitConverterAgent()
    result = agent.convert(args.value, args.src_unit, args.tgt_unit)

    if args.json:
        payload = {
            "input": {
                "value": args.value,
                "src_unit": args.src_unit,
                "tgt_unit": args.tgt_unit,
            },
            "output": result,
        }
        print(json.dumps(payload, ensure_ascii=False))
        return payload

    print(f"{args.value} {args.src_unit} = {result} {args.tgt_unit}")
    return result


if __name__ == "__main__":  # pragma: no cover
    main()
