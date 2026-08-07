"""
Assignment 11 — Audit Log starter (TODO).

Records every interaction for forensics. Never blocks by itself —
other layers catch attacks; this layer makes them reviewable.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path


class AuditLogPlugin:
    """Framework-agnostic audit logger (wire into ADK callbacks or your pipeline)."""

    def __init__(self):
        self.name = "audit_log"
        self.logs: list[dict] = []
        self._open: dict[str, float] = {}

    def record_input(self, *, user_id: str, text: str, request_id: str | None = None):
        """TODO: store input + start timestamp keyed by request_id/user_id."""
        self._open[request_id] = {"start_time": time.time()}
        self.logs.append({
            "request_id": request_id,
            "user_id": user_id,
            "input": text,
            "timestamp": utc_now_iso(),
        })

    def record_output(
        self,
        *,
        user_id: str,
        text: str,
        blocked: bool = False,
        layer: str | None = None,
        request_id: str | None = None,
    ):
        """TODO: store output, layer decision, latency; append to self.logs."""
        # Find the entry in logs
        for log in self.logs:
            if log.get("request_id") == request_id:
                start_time = self._open.get(request_id, {}).get("start_time", time.time())
                latency = time.time() - start_time
                log.update({
                    "output": text,
                    "blocked": blocked,
                    "layer": layer,
                    "latency": latency
                })
                break

    def export_json(self, filepath: str = "outputs/audit_log.json"):
        """Write logs to disk (JSON array)."""
        # TODO: ensure parent dirs exist, dump self.logs with indent=2
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
