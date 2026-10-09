"""Proofs for the sync feature.

The test below named for AC-SYNC-01 proves the offline change reaches a second
device; the one named for AC-OFFL-01 proves edits queue locally with no network.
(The proof-name tokens are only written as the actual function names, so the
Gate counts each proof exactly once.)

AC-SYNC-02 (disjoint-field merge) is intentionally NOT proved here — it is
tracked debt (open TODO T005). That is why the Gate reports it as tracked-debt,
not proven.
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
    assert elapsed < 2.0  # AC-SYNC-01: within 2s of reconnect


def test_AC_OFFL_01_edits_queue_locally_with_no_network():
    phone = Device("phone", online=False)

    phone.edit("item-1", "title", "Draft", ts=1.0)
    phone.edit("item-1", "done", "false", ts=2.0)
    phone.edit("item-2", "title", "Second", ts=3.0)

    # Fully usable offline: edits applied locally and nothing lost.
    assert len(phone.queue) == 3
    assert value_of(phone.items, "item-1", "title") == "Draft"
    assert value_of(phone.items, "item-2", "title") == "Second"
