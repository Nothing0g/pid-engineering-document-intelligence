import json
from pathlib import Path
from .models import Connection, Entity

class DocumentStore:
    def __init__(self, path: Path):
        self.payload = json.loads(path.read_text())

    def entities(self, revision: str) -> tuple[Entity, ...]:
        result = []
        for row in self.payload["entities"].get(revision, []):
            result.append(Entity(row["tag"], row["type"], row["label"], tuple(row["bbox"]), row["source_text"], float(row["confidence"]), review_status="accepted" if row["confidence"] >= 0.90 else "needs_review"))
        return tuple(result)

    def connections(self, revision: str, include_validation_case: bool = False) -> tuple[Connection, ...]:
        rows = list(self.payload["connections"].get(revision, []))
        if include_validation_case:
            rows += self.payload.get("validation_cases", {}).get(revision, [])
        return tuple(Connection(r["from"], r["to"], r["line"], r["label"]) for r in rows)

    def metadata(self, revision: str) -> dict:
        return self.payload["documents"][revision]
