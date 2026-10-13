import time
from .compare import compare_entities
from .graph import path_for
from .loader import DocumentStore
from .validate import validate
from .models import Entity

class PidService:
    def __init__(self, store: DocumentStore):
        self.store = store

    def extract(self, revision: str) -> dict:
        entities = self.store.entities(revision)
        connections = self.store.connections(revision)
        issues = validate(entities, connections)
        return {"document": self.store.metadata(revision), "entities": [_entity(e) for e in entities], "connections": [_connection(c) for c in connections], "issues": [_issue(i) for i in issues]}

    def compare(self, base: str, candidate: str) -> dict:
        return {"base": base, "candidate": candidate, "entity_changes": compare_entities(self.store.entities(base), self.store.entities(candidate))}

    def ask(self, revision: str, question: str) -> dict:
        started = time.perf_counter()
        entities = self.store.entities(revision)
        connections = self.store.connections(revision)
        upper = question.upper()
        mentioned = next((e.tag for e in entities if e.tag in upper), None)
        if mentioned:
            paths = path_for(mentioned, entities, connections)
            if paths:
                answer = f"{mentioned} is connected to " + ", ".join(f"{p['to']} via {p['line']} ({p['label']})" for p in paths) + "."
                return {"status":"answered", "answer":answer, "evidence":[{"tag":mentioned,"page":1,"bbox":next(e.bbox for e in entities if e.tag == mentioned),"source_text":next(e.source_text for e in entities if e.tag == mentioned)}] + [{"tag":p["to"],"page":1,"source_text":next(e.source_text for e in entities if e.tag == p["to"])} for p in paths], "human_review_required": any(e.confidence < 0.90 for e in entities if e.tag in {mentioned} | {p["to"] for p in paths}), "latency_ms": round((time.perf_counter()-started)*1000, 3)}
        return {"status":"needs_review", "answer":"I could not ground the question to an extracted entity. Review the drawing or ask using an equipment tag such as P-101.", "evidence":[], "human_review_required":True, "latency_ms":round((time.perf_counter()-started)*1000, 3)}

def _entity(e: Entity) -> dict:
    return {"tag":e.tag,"type":e.type,"label":e.label,"bbox":e.bbox,"source_text":e.source_text,"confidence":e.confidence,"page":e.page,"review_status":e.review_status}
def _connection(c) -> dict:
    return {"from":c.source,"to":c.target,"line":c.line,"label":c.label}
def _issue(i) -> dict:
    return {"code":i.code,"severity":i.severity,"message":i.message,"source":i.source,"target":i.target}
