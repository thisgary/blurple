import json
import dscord


def heartbeat() -> dscord.Payload:
    return dscord.Payload(1)


def identify(token: str) -> dscord.Payload:
    connection_properties = {
            '$os': 'linux', 
            '$browser': 'IE', 
            '$device': 'Nokia-3310'}
    return dscord.Payload(2, token=token, intents=32509, properties=conn_prop)


def resume(token: str, session_id: int, seq: int) -> dscord.Payload:
    return dscord.Payload(6, token=token, session_id=session_id, seq=seq)
