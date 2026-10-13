from .models import Entity

def compare_entities(base: tuple[Entity, ...], candidate: tuple[Entity, ...]) -> dict:
    base_map = {e.tag: e for e in base}
    candidate_map = {e.tag: e for e in candidate}
    added = sorted(set(candidate_map) - set(base_map))
    removed = []
    modified = []
    for tag in sorted(set(base_map) & set(candidate_map)):
        b, c = base_map[tag], candidate_map[tag]
        if b.type != c.type or b.label != c.label or b.bbox != c.bbox:
            modified.append({"tag": tag, "before": {"type": b.type, "label": b.label, "bbox": b.bbox}, "after": {"type": c.type, "label": c.label, "bbox": c.bbox}})
    return {"added": added, "removed": removed, "modified": modified, "changed_count": len(added) + len(removed) + len(modified)}
