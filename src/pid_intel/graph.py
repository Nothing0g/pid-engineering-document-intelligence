from .models import Connection, Entity

def adjacency(entities: tuple[Entity, ...], connections: tuple[Connection, ...]) -> dict[str, list[dict]]:
    tags = {e.tag for e in entities}
    graph = {tag: [] for tag in tags}
    for c in connections:
        if c.source in tags and c.target in tags:
            graph[c.source].append({"target": c.target, "line": c.line, "label": c.label})
    return graph

def path_for(tag: str, entities: tuple[Entity, ...], connections: tuple[Connection, ...]) -> list[dict]:
    tags = {e.tag for e in entities}
    return [{"from": c.source, "to": c.target, "line": c.line, "label": c.label} for c in connections if c.source == tag and c.target in tags]
