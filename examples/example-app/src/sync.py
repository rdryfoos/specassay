"""Cross-device sync for collaborative lists.

Two-way sync reconciles list changes across devices (FR-SYNC-01). Each device
keeps a local op queue so it stays fully usable offline; a central hub receives
queued ops on reconnect and fans the merged log back out.

Registry IDs served here live in ../PRD.md.
"""

from dataclasses import dataclass, field
import time


@dataclass
class Op:
    """A single field edit to a list item, stamped for ordering."""

    item_id: str
    field_name: str
    value: str
    ts: float


@dataclass
class Device:
    """A device holding a local copy of the list plus an outbound op queue."""

    name: str
    online: bool = True
    items: dict = field(default_factory=dict)   # item_id -> {field_name: value}
    queue: list = field(default_factory=list)   # ops not yet pushed to the hub

    def edit(self, item_id, field_name, value, ts=None):
        """Apply an edit locally and queue it. Works with or without a network.

        AC-OFFL-01: edits queue locally and apply optimistically even offline;
        nothing is lost while `online` is False.
        """
        op = Op(item_id, field_name, value, time.time() if ts is None else ts)
        merge_op(self.items, op)
        self.queue.append(op)
        return op


class SyncHub:
    """Central reconciliation point (stands in for the server)."""

    def __init__(self):
        self.log = []  # global, append-only op log

    # @covers AC-SYNC-01 — reconcile queued ops on the reconnect edge so an
    # offline change lands on every peer's next reconcile.
    def reconcile(self, device):
        """Push a device's queue to the hub, then merge the full log back in.

        No-op while the device is offline (nothing to reconnect to). Returns the
        ops delivered to the device this round.
        """
        if not device.online:
            return []
        self.log.extend(device.queue)
        device.queue = []
        for op in sorted(self.log, key=lambda o: o.ts):
            merge_op(device.items, op)
        return list(self.log)


# @covers AC-SYNC-02 — field-level merge: disjoint fields never collide; a
# same-field collision resolves last-write-wins by timestamp.
def merge_op(items, op):
    """Merge one op into an items map, keeping per-field write timestamps."""
    rec = items.setdefault(op.item_id, {})
    stamps = rec.setdefault("__ts__", {})
    if op.ts >= stamps.get(op.field_name, float("-inf")):
        rec[op.field_name] = op.value
        stamps[op.field_name] = op.ts
    return rec


def value_of(items, item_id, field_name):
    """Read a merged field value (ignores the internal timestamp bookkeeping)."""
    return items.get(item_id, {}).get(field_name)
