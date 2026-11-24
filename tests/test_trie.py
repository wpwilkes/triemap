"""Tests for the public Trie interface."""

import random
from collections.abc import MutableMapping
from typing import Any

import pytest

from triemap import Trie


@pytest.fixture
def trie() -> Trie[int]:
    return Trie({"car": 1, "cart": 2, "cat": 3, "dog": 4})


def test_empty_trie() -> None:
    empty: Trie[int] = Trie()

    assert isinstance(empty, MutableMapping)
    assert len(empty) == 0
    assert not empty
    assert list(empty) == []
    assert not empty.has_prefix("")


def test_initialize_from_mapping() -> None:
    assert dict(Trie({"car": 1, "cat": 2})) == {
        "car": 1,
        "cat": 2,
    }


def test_initialize_from_pairs() -> None:
    assert dict(Trie([("car", 1), ("car", 2)])) == {
        "car": 2,
    }


def test_insert_and_retrieve(trie: Trie[int]) -> None:
    trie["care"] = 5

    assert trie["care"] == 5
    assert trie["car"] == 1
    assert len(trie) == 5


def test_overwrite(trie: Trie[int]) -> None:
    trie["car"] = 10

    assert trie["car"] == 10
    assert len(trie) == 4


@pytest.mark.parametrize("key", ["missing", "ca", ""])
def test_missing_key(trie: Trie[int], key: str) -> None:
    with pytest.raises(KeyError) as error:
        _ = trie[key]

    assert error.value.args == (key,)

    with pytest.raises(KeyError):
        del trie[key]

    assert len(trie) == 4
    assert key not in trie


def test_membership(trie: Trie[int]) -> None:
    assert "car" in trie
    assert "ca" not in trie


@pytest.mark.parametrize(
    ("key", "remaining"),
    [
        ("cart", {"car": 1, "cat": 3, "dog": 4}),
        ("car", {"cart": 2, "cat": 3, "dog": 4}),
        ("cat", {"car": 1, "cart": 2, "dog": 4}),
        ("dog", {"car": 1, "cart": 2, "cat": 3}),
    ],
)
def test_delete(
    trie: Trie[int],
    key: str,
    remaining: dict[str, int],
) -> None:
    del trie[key]

    assert key not in trie
    assert dict(trie) == remaining
    assert len(trie) == len(remaining)


def test_pruning() -> None:
    trie = Trie({"car": 1, "cart": 2})

    del trie["car"]

    assert trie.has_prefix("car")

    del trie["cart"]

    assert not trie.has_prefix("c")
    assert not trie.has_prefix("")
    assert len(trie) == 0


def test_iteration(trie: Trie[int]) -> None:
    keys = list(trie)

    assert len(keys) == len(set(keys)) == len(trie)
    assert set(keys) == {"car", "cart", "cat", "dog"}


@pytest.mark.parametrize(
    ("prefix", "expected"),
    [
        ("", {"car": 1, "cart": 2, "cat": 3, "dog": 4}),
        ("ca", {"car": 1, "cart": 2, "cat": 3}),
        ("car", {"car": 1, "cart": 2}),
        ("cart", {"cart": 2}),
        ("xyz", {}),
    ],
)
def test_prefix_search(
    trie: Trie[int],
    prefix: str,
    expected: dict[str, int],
) -> None:
    assert trie.has_prefix(prefix) == bool(expected)

    assert sorted(trie.keys_with_prefix(prefix)) == sorted(expected)

    items = list(trie.items_with_prefix(prefix))

    assert len(items) == len(expected)
    assert dict(items) == expected


def test_clear(trie: Trie[int]) -> None:
    trie.clear()

    assert len(trie) == 0
    assert list(trie) == []
    assert not trie.has_prefix("")

    trie["new"] = 5

    assert dict(trie) == {"new": 5}


def test_mapping_methods(trie: Trie[int]) -> None:
    assert trie.get("car") == 1
    assert trie.get("missing", 0) == 0

    assert trie.setdefault("car", 10) == 1
    assert trie.setdefault("bird", 5) == 5

    trie.update({"car": 10, "fish": 6})

    assert trie.pop("dog") == 4
    assert trie.pop("missing", 0) == 0

    expected = {
        "car": 10,
        "cart": 2,
        "cat": 3,
        "bird": 5,
        "fish": 6,
    }

    assert trie == expected
    assert set(trie.keys()) == set(expected)
    assert sorted(trie.values()) == sorted(expected.values())
    assert dict(trie.items()) == expected

    key, value = trie.popitem()

    assert expected.pop(key) == value
    assert dict(trie) == expected


def test_empty_key(trie: Trie[int]) -> None:
    trie[""] = 0

    assert trie[""] == 0
    assert "" in trie
    assert len(trie) == 5

    del trie[""]

    assert "" not in trie
    assert trie.has_prefix("")
    assert len(trie) == 4


def test_none_value() -> None:
    trie: Trie[int | None] = Trie({"car": None, "cart": 2})

    assert trie["car"] is None
    assert "car" in trie

    assert dict(trie.items_with_prefix("car")) == {
        "car": None,
        "cart": 2,
    }

    del trie["car"]

    assert "car" not in trie
    assert trie["cart"] == 2


def test_unicode_and_case_sensitivity() -> None:
    trie = Trie({"Cat": 1, "cat": 2, "café": 3, "猫": 4})

    assert trie["Cat"] == 1
    assert trie["cat"] == 2
    assert trie["猫"] == 4
    assert set(trie.keys_with_prefix("ca")) == {"cat", "café"}


def test_invalid_key_types(trie: Trie[int]) -> None:
    key: Any = 123

    with pytest.raises(TypeError):
        trie[key] = 1

    with pytest.raises(TypeError):
        _ = trie[key]

    with pytest.raises(TypeError):
        del trie[key]

    with pytest.raises(TypeError):
        trie.has_prefix(key)

    with pytest.raises(TypeError):
        list(trie.keys_with_prefix(key))

    with pytest.raises(TypeError):
        list(trie.items_with_prefix(key))

    assert key not in trie
    assert len(trie) == 4


def test_deep_trie() -> None:
    key = "a" * 5000
    trie = Trie({key: 1})

    assert trie[key] == 1
    assert list(trie) == [key]
    assert list(trie.keys_with_prefix("aaa")) == [key]

    del trie[key]

    assert not trie


def test_against_dict() -> None:
    rng = random.Random(42)

    trie: Trie[int] = Trie()
    expected: dict[str, int] = {}

    keys = ["", "a", "ab", "abc", "b", "ba", "cab", "cat", "car"]

    for _ in range(250):
        key = rng.choice(keys)

        if rng.choice([True, False]):
            value = rng.randrange(100)

            trie[key] = value
            expected[key] = value

        elif key in expected:
            del trie[key]
            del expected[key]

        else:
            with pytest.raises(KeyError):
                del trie[key]

        assert len(trie) == len(expected)
        assert dict(trie) == expected

        prefix = rng.choice(keys)

        assert dict(trie.items_with_prefix(prefix)) == {
            k: v for k, v in expected.items() if k.startswith(prefix)
        }
