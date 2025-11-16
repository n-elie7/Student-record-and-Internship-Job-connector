from setup_env import supabase as sb

_realtime_flags = {"students": False, "internships": False, "applications": False}


def _payload_printer(payload):
    # payload is a dict with keys: 'schema','table','eventType','record', ...
    try:
        table = payload.get("table") or payload.get("table")
        ev = payload.get("type") or payload.get("eventType") or payload.get("event")
        record = payload.get("record") or payload.get("new") or payload.get("row")
        print("\n[Realtime update] table:", table, "event:", ev)
        if record:
            print(" ->", record)
        # set flag to indicate data changed (optional use in UI)
        if table in _realtime_flags:
            _realtime_flags[table] = True
    except Exception as e:
        print("[Realtime] Error handling payload:", e)


def start_realtime_listener():
    """
    Start realtime subscriptions in a background thread.
    Subscribes to students, internships, applications for INSERT/UPDATE/DELETE.
    """
    # channel name arbitrary
    channel = sb.channel("sric_changes_channel")
    # on postgres_changes event object payload contains keys like: schema, table, type, record
    for tbl in ("students", "internships", "applications"):
        for ev in ("INSERT", "UPDATE", "DELETE"):
            channel.on(
                "postgres_changes",
                {"event": ev, "schema": "public", "table": tbl},
                lambda payload, tbl=tbl, ev=ev: _payload_printer(
                    {
                        "table": tbl,
                        "event": ev,
                        "record": payload.get("record")
                        if isinstance(payload, dict)
                        else payload,
                    }
                ),
            )
    channel.subscribe()
    print("[Realtime] Subscribed to table changes (students/internships/applications).")
