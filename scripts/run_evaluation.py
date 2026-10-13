import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from pid_intel.config import DATA_PATH, REPORT_PATH
from pid_intel.loader import DocumentStore
from pid_intel.service import PidService
from pid_intel.validate import validate

service = PidService(DocumentStore(DATA_PATH))
start = time.perf_counter()
extract = service.extract('rev-b')
compare = service.compare('rev-a','rev-b')
answer = service.ask('rev-b','What is connected to P-101?')
validation = validate(service.store.entities('rev-b'), service.store.connections('rev-b', include_validation_case=True))
report = {
  'synthetic': True,
  'checks': {
    'entity_count_is_five': len(extract['entities']) == 5,
    'all_entities_have_source_evidence': all(e['source_text'] and len(e['bbox']) == 4 for e in extract['entities']),
    'added_instrument_detected': compare['entity_changes']['added'] == ['FT-101'],
    'removed_instrument_detected': compare['entity_changes']['removed'] == ['PT-101'],
    'dangling_connection_flagged': any(i.code == 'DANGLING_CONNECTION' for i in validation),
    'answer_has_evidence': answer['status'] == 'answered' and len(answer['evidence']) >= 2,
    'unknown_question_abstains': service.ask('rev-b','What is the relief valve set pressure?')['human_review_required'],
  },
  'metrics': {'entity_count': len(extract['entities']), 'revision_changes': compare['entity_changes']['changed_count'], 'validation_issue_count': len(validation), 'answer_latency_ms': answer['latency_ms'], 'evaluation_runtime_ms': round((time.perf_counter()-start)*1000,3)},
  'limitations': ['Synthetic SVG and metadata are not a benchmark for arbitrary scanned P&IDs.', 'The current extractor is a deterministic adapter; OCR and symbol recognition are extension points.', 'Engineering rules require review against project-specific standards.']
}
REPORT_PATH.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
