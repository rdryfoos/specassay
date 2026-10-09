"""Proofs for the sync feature.

The test below named for AC-SYNC-01 proves the offline change reaches a second
device; the one named for AC-OFFL-01 proves edits queue locally with no network.
(The proof-name tokens are only written as the actual function names, so the
Gate counts each proof exactly once.)

AC-SYNC-02 (disjoint-field merge) is proved by test_AC_SYNC_02_* below: two
devices editing different fields of the same item both survive the merge.
"""

import time

from src.sync import Device, SyncHub, value_of


def test_AC_SYNC_01_offline_change_appears_on_second_device():
    hub = SyncHub()
    phone = Device("phone")
    laptop = Device("laptop")

    # Phone goes offline and edits a list item.
    phone.online = False
    phone.edit("item-1", "title", "Buy oat milk", ts=1.0)
    assert value_of(phone.items, "item-1", "title") == "Buy oat milk"

    # Reconnect edge: reconcile propagates through the hub within budget.
    start = time.monotonic()
    phone.online = True
    hub.reconcile(phone)
    laptop.online = True
    hub.reconcile(laptop)
    elapsed = time.monotonic() - start

    assert value_of(laptop.items, "item-1", "title") == "Buy oat milk"
    assert elapsed < 5.0  # AC-SYNC-01: within 5s of reconnect


def test_AC_OFFL_01_edits_queue_locally_with_no_network():
    phone = Device("phone", online=False)

    phone.edit("item-1", "title", "Draft", ts=1.0)
    phone.edit("item-1", "done", "false", ts=2.0)
    phone.edit("item-2", "title", "Second", ts=3.0)

    # Fully usable offline: edits applied locally and nothing lost.
    assert len(phone.queue) == 3
    assert value_of(phone.items, "item-1", "title") == "Draft"
    assert value_of(phone.items, "item-2", "title") == "Second"


def test_AC_SYNC_02_disjoint_field_edits_merge_without_conflict():
    hub = SyncHub()
    a = Device("a")
    b = Device("b")

    # Two devices edit DIFFERENT fields of the same item, unaware of each other.
    a.edit("item-1", "title", "Buy milk", ts=1.0)
    b.edit("item-1", "done", "true", ts=2.0)

    # Reconcile both through the hub; each pulls the other's op.
    hub.reconcile(a)
    hub.reconcile(b)
    hub.reconcile(a)

    # AC-SYNC-02: disjoint fields both survive — neither clobbers the other.
    for dev in (a, b):
        assert value_of(dev.items, "item-1", "title") == "Buy milk"
        assert value_of(dev.items, "item-1", "done") == "true"
