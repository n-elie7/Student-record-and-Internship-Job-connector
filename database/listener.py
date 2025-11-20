import asyncio
import threading
from supabase import acreate_client

_realtime_flags = {"students": False, "internships": False, "applications": False}
_change_detected = False


def _payload_printer(payload):
    global _change_detected
    try:
        table = payload.get("table")
        ev = payload.get("type") or payload.get("eventType") or payload.get("event")
        record = payload.get("record") or payload.get("new") or payload.get("row")

        if record:
            print(f"   → {record}")
        if table in _realtime_flags:
            _realtime_flags[table] = True
        _change_detected = True
    except Exception as e:
        print(f"[Realtime] Error: {e}")


async def async_realtime_listener():
    """Async function to listen for realtime changes"""
    from setup_env import SUPABASE_URL, SUPABASE_ANON_KEY

    supabase = await acreate_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    channel = supabase.channel("sric_changes_channel")

    for tbl in ("students", "internships", "applications"):
        for ev in ("INSERT", "UPDATE", "DELETE"):
            channel.on_postgres_changes(
                event=ev,
                schema="public",
                table=tbl,
                callback=lambda payload, t=tbl, e=ev: _payload_printer(
                    {
                        "table": t,
                        "event": e,
                        "record": payload.get("record")
                        if isinstance(payload, dict)
                        else payload,
                    }
                ),
            )

    await channel.subscribe()

    # Keep connection alive
    while True:
        await asyncio.sleep(1)


def start_realtime_listener():
    """Start realtime listener in background thread with new event loop"""

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_realtime_listener())
        except Exception as e:
            print(f"[Realtime] Error: {e}")

    t = threading.Thread(target=run_async, daemon=True)
    t.start()
