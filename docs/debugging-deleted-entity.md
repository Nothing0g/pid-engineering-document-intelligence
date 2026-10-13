# Debugging note: deleted entities in revision comparison

## Symptom

The first revision comparator reported that `FT-101` was added in revision B but failed to report that `PT-101` had been removed. That would make a drawing review incomplete: replacing an instrument is materially different from only adding one.

## Root cause

The prototype iterated only over candidate entities. It could see additions, but it had no loop over base-only tags, so deletion information was lost.

## Fix

The final comparator computes both set differences:

```python
added = sorted(set(candidate_map) - set(base_map))
removed = sorted(set(base_map) - set(candidate_map))
```

The regression test now asserts both `FT-101` added and `PT-101` removed. The captured failed run is preserved in `reports/debug/deleted-entity-failure.txt`.

## Lesson

Revision comparison must be symmetric. A document-review system that reports additions but misses removals can create false confidence.
