"""A minimal unit converter agent implemented with the OpenAI Agent SDK."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .converter import convert

try:  # The OpenAI Agent SDK is optional at runtime.
    from openai import OpenAI
    from openai.agents import Agent, tool
except Exception:  # pragma: no cover - import errors are handled gracefully.
    OpenAI = None  # type: ignore[assignment]
    Agent = None  # type: ignore[assignment]

    def tool(func):  # type: ignore[misc]
        """Fallback decorator when the SDK is unavailable."""

        return func


@dataclass
class UnitConverterAgent:
    """Minimal helper around the conversion logic.

    When an :class:`~openai.OpenAI` client is supplied the class also exposes a
    ready-to-use :class:`~openai.agents.Agent` instance that can be used to
    orchestrate conversations and tool calls. The conversion itself is performed
    locally using predefined ratios and does not require network access.
    """

    client: Optional["OpenAI"] = None
    model: str = "gpt-4.1-mini"

    def __post_init__(self) -> None:
        self._agent: Optional["Agent"] = None
        if self.client is not None and Agent is not None:
            self._agent = Agent(
                client=self.client,
                model=self.model,
                instructions=(
                    "You are a unit conversion assistant. Rely on the provided "
                    "convert_units tool for calculations and echo only the "
                    "numeric result."
                ),
                tools=[convert_units],
            )

    @property
    def agent(self) -> Optional["Agent"]:
        """Expose the lazily created Agent instance (if available)."""

        return self._agent

    def convert(self, value: float, src_unit: str, tgt_unit: str) -> float:
        """Perform a unit conversion locally."""

        return convert(value=value, src_unit=src_unit, tgt_unit=tgt_unit)


@tool
def convert_units(value: float, src_unit: str, tgt_unit: str) -> str:
    """Tool wrapper that delegates to :func:`unit_converter_agent.converter.convert`."""

    result = convert(value=value, src_unit=src_unit, tgt_unit=tgt_unit)
    return f"{result}"


__all__ = ["UnitConverterAgent", "convert_units"]
