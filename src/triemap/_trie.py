"""Implementation of the trie data structure."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from typing import TypeVar, cast

from ._node import Node

V = TypeVar("V")


class Trie(MutableMapping[str, V]):
    """A mutable string-keyed mapping implemented as a prefix tree."""

    def __init__(
        self,
        initial: Mapping[str, V] | Iterable[tuple[str, V]] = (),
    ) -> None:
        self._root: Node[V] = Node()
        self._size = 0
        self.update(initial)

    def __getitem__(self, key: str) -> V:
        node = self._findNode(key)

        if node is None or not node.terminal:
            raise KeyError(key)

        return cast(V, node.value)

    def __setitem__(self, key: str, value: V) -> None:
        self._validate_key(key)
        current = self._root

        for char in key:
            if char not in current.children:
                current.children[char] = Node()

            current = current.children[char]

        if not current.terminal:
            self._size += 1

        current.value = value
        current.terminal = True

    def __delitem__(self, key: str) -> None:
        self._validate_key(key)
        current = self._root
        path: list[tuple[Node[V], str]] = []

        for char in key:
            child = current.children.get(char)

            if child is None:
                raise KeyError(key)

            path.append((current, char))
            current = child

        if not current.terminal:
            raise KeyError(key)

        current.value = None
        current.terminal = False
        self._size -= 1

        for parent, char in reversed(path):
            child = parent.children[char]

            if child.terminal or child.children:
                break

            del parent.children[char]

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False

        node = self._findNode(key)

        return node is not None and node.terminal

    def __iter__(self) -> Iterator[str]:
        return self.keys_with_prefix("")

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        """Remove all entries from the trie."""
        self._root = Node()
        self._size = 0

    def has_prefix(self, prefix: str) -> bool:
        """Return whether any stored key begins with the prefix."""
        node = self._findNode(prefix)

        return node is not None and (node.terminal or bool(node.children))

    def keys_with_prefix(self, prefix: str) -> Iterator[str]:
        """Iterate over stored keys beginning with the prefix."""
        return (key for key, _ in self.items_with_prefix(prefix))

    def items_with_prefix(
        self,
        prefix: str,
    ) -> Iterator[tuple[str, V]]:
        """Iterate over key-value pairs beginning with the prefix."""
        node = self._findNode(prefix)

        if node is None:
            return iter(())

        return self._iter_items(node, prefix)

    def _findNode(self, key: str) -> Node[V] | None:
        """Locate the node corresponding to a string."""
        self._validate_key(key)
        current = self._root

        for char in key:
            child = current.children.get(char)

            if child is None:
                return None

            current = child

        return current

    @staticmethod
    def _iter_items(
        node: Node[V],
        prefix: str,
    ) -> Iterator[tuple[str, V]]:
        """Traverse a subtree using iterative depth-first search."""
        suffix: list[str] = []
        stack = [iter(node.children.items())]

        if node.terminal:
            yield prefix, cast(V, node.value)

        while stack:
            try:
                char, child = next(stack[-1])
            except StopIteration:
                stack.pop()

                if suffix:
                    suffix.pop()

                continue

            suffix.append(char)
            stack.append(iter(child.children.items()))

            if child.terminal:
                key = prefix + "".join(suffix)
                yield key, cast(V, child.value)

    @staticmethod
    def _validate_key(key: str) -> None:
        """Ensure that a key is a string."""
        if not isinstance(key, str):
            raise TypeError("Trie keys must be strings.")
