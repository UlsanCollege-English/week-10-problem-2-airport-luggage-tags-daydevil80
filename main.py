"""
HW02 — Airport Luggage Tags (Open Addressing with Delete)
Implement linear probing with EMPTY and DELETED markers.
"""

# Step 4: create unique marker objects
EMPTY = object()
DELETED = object()

def _hash(key, m):
    """Simple deterministic hash."""
    return sum(ord(c) for c in key) % m

def make_table_open(m):
    """Return a table of length m filled with EMPTY markers."""
    return [EMPTY for _ in range(m)]

def _find_slot_for_insert(t, key):
    """Return index to insert/overwrite (may return DELETED slot). Return None if full."""
    m = len(t)
    first_deleted = None
    start = _hash(key, m)

    for i in range(m):
        idx = (start + i) % m
        entry = t[idx]
        if entry is EMPTY:
            # If we saw a deleted earlier, return that
            return first_deleted if first_deleted is not None else idx
        elif entry is DELETED:
            if first_deleted is None:
                first_deleted = idx
        elif entry[0] == key:
            return idx
    return first_deleted  # if full and we saw deleted; else None

def _find_slot_for_search(t, key):
    """Return index where key is found; else None. DELETED does not stop search."""
    m = len(t)
    start = _hash(key, m)

    for i in range(m):
        idx = (start + i) % m
        entry = t[idx]
        if entry is EMPTY:
            # EMPTY means key was never here
            return None
        elif entry is DELETED:
            # skip deleted — continue probing
            continue
        elif entry[0] == key:
            return idx
    return None

def put_open(t, key, value):
    """Insert or overwrite (key, value). Return True on success, False if table is full."""
    idx = _find_slot_for_insert(t, key)
    if idx is None:
        return False
    t[idx] = (key, value)
    return True

def get_open(t, key):
    """Return value for key or None if not present."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return None
    entry = t[idx]
    if entry is EMPTY or entry is DELETED:
        return None
    return entry[1]

def delete_open(t, key):
    """Delete key if present. Return True if removed, else False."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return False
    if t[idx] is EMPTY or t[idx] is DELETED:
        return False
    t[idx] = DELETED
    return True

if __name__ == "__main__":
    # Manual test
    t = make_table_open(5)
    print("put_open:", put_open(t, "A1", "bag1"))
    print("get_open:", get_open(t, "A1"))
    print("delete_open:", delete_open(t, "A1"))
    print("get_open after delete:", get_open(t, "A1"))
