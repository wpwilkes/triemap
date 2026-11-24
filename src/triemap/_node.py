from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

V = TypeVar("V")


@dataclass(slots=True, eq=False)
class Node(Generic[V]):
    """Internal node of a trie."""

    children: dict[str, Node[V]] = field(default_factory=dict)
    value: V | None = None
    terminal: bool = False
