# TrieMap

[![CI](https://github.com/wpwilkes/triemap/actions/workflows/ci.yml/badge.svg)](https://github.com/wpwilkes/triemap/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)

A lightweight, typed implementation of the trie (prefix tree) data structure
for Python.

TrieMap provides a mutable string-keyed mapping with efficient prefix
search, a familiar dictionary-like interface, and no runtime dependencies.

## Features

- Standard Python `MutableMapping` interface.
- Efficient insertion, retrieval, and deletion.
- Prefix-based key and value enumeration.
- Generic value types and inline type annotations.
- Iterative traversal without recursion-depth limitations.
- Unicode and empty-string key support.
- Zero runtime dependencies.

## Installation

TrieMap requires Python 3.10 or later.

Install directly from GitHub:

```bash
pip install git+https://github.com/wpwilkes/triemap.git
```

## Usage

### Basic operations

```python
from triemap import Trie

trie: Trie[int] = Trie()

trie["car"] = 1
trie["cart"] = 2
trie["cat"] = 3

assert trie["car"] == 1
assert "cart" in trie
assert len(trie) == 3

del trie["cart"]

assert "cart" not in trie
assert "car" in trie
```

### Initialization

A trie can be initialized from a mapping or an iterable of key-value pairs.

```python
trie = Trie(
    {
        "car": 1,
        "cart": 2,
        "cat": 3,
    }
)
```

### Prefix search

```python
trie = Trie(
    {
        "car": 1,
        "cart": 2,
        "cat": 3,
        "dog": 4,
    }
)

trie.has_prefix("ca")
# True

sorted(trie.keys_with_prefix("ca"))
# ['car', 'cart', 'cat']

dict(trie.items_with_prefix("car"))
# {'car': 1, 'cart': 2}
```

Prefix enumeration returns lazy iterators rather than materialized lists.

### Mapping interface

TrieMap implements `collections.abc.MutableMapping` and supports
standard mapping operations.

```python
trie.get("car")
trie.setdefault("bird", 5)
trie.update({"fish": 6})
trie.pop("dog")
trie.keys()
trie.values()
trie.items()
trie.clear()
```

### Type annotations

The value type can be specified using Python's generic type syntax.

```python
trie: Trie[int] = Trie()
trie["apple"] = 1

names: Trie[str] = Trie()
names["smith"] = "John Smith"
```

TrieMap includes a `py.typed` marker for compatibility with static
type checkers.

## Data Structure

A trie is a rooted tree in which edges are labeled by characters.
Each path from the root represents a string, and terminal nodes
represent stored keys.

For example, the keys `car`, `cart`, `cat`, and `dog` produce
the following structure:

```text
(root)
├── c
│   └── a
│       ├── r [1]
│       │   └── t [2]
│       └── t [3]
└── d
    └── o
        └── g [4]
```

Bracketed numbers denote values associated with terminal nodes.

Keys sharing a common prefix share the corresponding portion of the
tree. This permits prefix queries without examining every stored key.

Deletion removes the terminal designation of a key and prunes
nodes that are no longer required.

## API Reference

| Method | Description |
| :--- | :--- |
| `Trie(initial=())` | Initialize a trie. |
| `trie[key]` | Retrieve the value associated with a key. |
| `trie[key] = value` | Insert or update a key-value pair. |
| `del trie[key]` | Remove a key-value pair. |
| `key in trie` | Test exact key membership. |
| `len(trie)` | Return the number of stored keys. |
| `iter(trie)` | Iterate over stored keys. |
| `trie.clear()` | Remove all entries. |
| `trie.has_prefix(prefix)` | Test whether a stored key begins with a prefix. |
| `trie.keys_with_prefix(prefix)` | Iterate over matching keys. |
| `trie.items_with_prefix(prefix)` | Iterate over matching key-value pairs. |

Standard methods inherited from `MutableMapping`, including `get`,
`update`, `pop`, `popitem`, `setdefault`, `keys`, `values`, and
`items`, are also available.

### Behavior

- Keys must be strings.
- Keys are case-sensitive.
- Empty strings are valid keys.
- `None` is a valid value when permitted by the declared value type.
- Retrieving or deleting a missing key raises `KeyError`.
- Non-string keys raise `TypeError` when used for retrieval,
  insertion, deletion, or prefix queries.
- Non-string membership queries return `False`.
- Iteration follows depth-first traversal order rather than
  insertion or lexicographic order.


## Computational Complexity

Let:

- `k` be the length of a key or prefix.
- `s` be the number of nodes in the traversed subtree.
- `h` be the maximum depth of the traversed subtree.
- `L` be the total length of the returned keys.

| Operation          | Time Complexity | Auxiliary Space |
| :----------------- | :-------------: | :-------------: |
| Insertion          | `O(k)`          | `O(1)`          |
| Retrieval          | `O(k)`          | `O(1)`          |
| Deletion           | `O(k)`          | `O(k)`          |
| Membership         | `O(k)`          | `O(1)`          |
| Length             | `O(1)`          | `O(1)`          |
| Prefix existence   | `O(k)`          | `O(1)`          |
| Prefix enumeration | `O(k + s + L)`  | `O(h + 1)`      |

These bounds assume average constant-time dictionary operations.
Auxiliary space excludes newly allocated tree nodes and emitted results.

Total storage is linear in the number of distinct prefixes,
including the root, excluding the storage required by associated values.


## Development

Clone the repository and create a virtual environment.

```bash
git clone https://github.com/wpwilkes/triemap.git
cd triemap

python -m venv .venv
source .venv/bin/activate

python -m pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

Run tests with coverage reporting:

```bash
pytest --cov=triemap --cov-report=term-missing
```

### Code Quality

```bash
ruff check .
ruff format --check .
mypy
```

### Building

```bash
python -m build
python -m twine check --strict dist/*
```

## License

TrieMap is distributed under the GNU General Public License v3.0.

See [LICENSE](LICENSE) for details.
