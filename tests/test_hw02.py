
import sys, os, random
# ✅ ensure we can import main.py from parent folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import make_table_open, put_open, get_open, delete_open

# ---- Normal tests (4) ----

def test_basic_put_get():
    t = make_table_open(7)
    assert put_open(t, "TAG1", "loaded") is True
    assert get_open(t, "TAG1") == "loaded"

def test_overwrite_value():
    t = make_table_open(5)
    put_open(t, "T1", "ready")
    put_open(t, "T1", "done")
    assert get_open(t, "T1") == "done"

def test_linear_probe_wrap():
    t = make_table_open(3)
    # Force collisions by same hash % 3
    assert put_open(t, "AA", "x")
    assert put_open(t, "BB", "y")
    assert put_open(t, "CC", "z")
    # Table is full; lookups still work
    assert get_open(t, "BB") == "y"

def test_delete_then_reinsert():
    t = make_table_open(5)
    put_open(t, "K1", "a")
    put_open(t, "K2", "b")
    assert delete_open(t, "K1") is True
    assert get_open(t, "K1") is None
    assert put_open(t, "K3", "c") is True  # can reuse DELETED

# ---- Edge-case tests (3) ----

def test_delete_missing_returns_false():
    t = make_table_open(4)
    assert delete_open(t, "NOPE") is False

def test_table_full_put_returns_false():
    t = make_table_open(3)
    assert put_open(t, "A", "1")
    assert put_open(t, "B", "2")
    assert put_open(t, "C", "3")
    assert put_open(t, "D", "4") in (False, None)

def test_search_skips_deleted_slots():
    t = make_table_open(5)
    put_open(t, "A", "1")
    put_open(t, "B", "2")
    delete_open(t, "A")
    # A is deleted; searching B must not stop at deleted
    assert get_open(t, "B") == "2"

# ---- More-complex tests (3) ----

def test_many_ops_with_interleaved_deletes():
    t = make_table_open(17)
    keys = [f"K{i}" for i in range(12)]
    for k in keys:
        assert put_open(t, k, k.lower())
    for k in keys[::2]:
        assert delete_open(t, k) is True
    for k in keys[1::2]:
        assert get_open(t, k) == k.lower()
    for i in range(6):
        assert put_open(t, f"NEW{i}", str(i)) is True

def test_reinsert_over_deleted_then_lookup_all():
    t = make_table_open(11)
    for i in range(7):
        put_open(t, f"x{i}", str(i))
    delete_open(t, "x3")
    delete_open(t, "x4")
    put_open(t, "x13", "13")
    assert get_open(t, "x13") == "13"
    assert get_open(t, "x3") is None

def test_overwrite_after_probe_chain():
    t = make_table_open(7)
    for k in ["A0","B1","C2","D3"]:
        put_open(t, k, k)
    put_open(t, "A0", "Z")
    assert get_open(t, "A0") == "Z"
