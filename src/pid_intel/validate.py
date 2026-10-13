from .models import Connection, Entity, ValidationIssue

def validate(entities: tuple[Entity, ...], connections: tuple[Connection, ...]) -> tuple[ValidationIssue, ...]:
    tags = {e.tag for e in entities}
    issues = []
    for entity in entities:
        if entity.confidence < 0.90:
            issues.append(ValidationIssue("LOW_CONFIDENCE", "warning", f"{entity.tag} needs human review before use.", entity.tag, None))
    for c in connections:
        if c.source not in tags or c.target not in tags:
            issues.append(ValidationIssue("DANGLING_CONNECTION", "error", f"{c.line} connects unresolved entities: {c.source} -> {c.target}.", c.source, c.target))
    return tuple(issues)
