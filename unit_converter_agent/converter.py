"""Core conversion logic for the unit converter agent."""
from __future__ import annotations

from dataclasses import dataclass


class UnknownUnitError(ValueError):
    """Raised when an unsupported unit is requested."""


class IncompatibleUnitError(ValueError):
    """Raised when two units of different dimensions are combined."""


@dataclass(frozen=True)
class ConversionCategory:
    """Holds conversion factors for a specific measurement category."""

    base_unit: str
    factors: dict[str, float]

    def normalise(self, unit: str) -> float:
        try:
            return self.factors[unit]
        except KeyError as exc:
            raise UnknownUnitError(f"Unsupported unit: {unit}") from exc


_LENGTH_CATEGORY = ConversionCategory(
    base_unit="m",
    factors={
        "km": 1000.0,
        "m": 1.0,
        "cm": 0.01,
        "mm": 0.001,
        "mile": 1609.344,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
    },
)

_WEIGHT_CATEGORY = ConversionCategory(
    base_unit="kg",
    factors={
        "kg": 1.0,
        "g": 0.001,
        "lb": 0.45359237,
        "oz": 0.0283495231,
    },
)


_CATEGORIES: dict[str, ConversionCategory] = {
    unit: _LENGTH_CATEGORY for unit in _LENGTH_CATEGORY.factors
}
_CATEGORIES.update({unit: _WEIGHT_CATEGORY for unit in _WEIGHT_CATEGORY.factors})


def convert(value: float, src_unit: str, tgt_unit: str) -> float:
    """Convert *value* from *src_unit* into *tgt_unit*.

    Args:
        value: The numeric value to convert.
        src_unit: The unit of the supplied value.
        tgt_unit: The desired output unit.

    Returns:
        The converted numeric value.

    Raises:
        UnknownUnitError: If either the source or target unit is unsupported.
        IncompatibleUnitError: If the units belong to different categories.
    """

    normalised_src = src_unit.lower()
    normalised_tgt = tgt_unit.lower()

    try:
        src_category = _CATEGORIES[normalised_src]
    except KeyError as exc:
        raise UnknownUnitError(f"Unsupported unit: {src_unit}") from exc

    try:
        tgt_category = _CATEGORIES[normalised_tgt]
    except KeyError as exc:
        raise UnknownUnitError(f"Unsupported unit: {tgt_unit}") from exc

    if src_category is not tgt_category:
        raise IncompatibleUnitError(
            f"Cannot convert between '{src_unit}' and '{tgt_unit}' because they belong to different dimensions."
        )

    value_in_base = value * src_category.normalise(normalised_src)
    return value_in_base / src_category.normalise(normalised_tgt)


__all__ = [
    "convert",
    "ConversionCategory",
    "IncompatibleUnitError",
    "UnknownUnitError",
]
