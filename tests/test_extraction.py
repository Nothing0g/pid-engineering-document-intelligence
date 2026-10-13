from pid_intel.config import DATA_PATH
from pid_intel.loader import DocumentStore
from pid_intel.service import PidService

def service(): return PidService(DocumentStore(DATA_PATH))

def test_revision_b_extracts_typed_entities():
    result = service().extract('rev-b')
    assert len(result['entities']) == 5
    assert {e['tag'] for e in result['entities']} == {'TK-101','P-101','V-201','E-101','FT-101'}

def test_question_is_evidence_linked():
    result = service().ask('rev-b', 'What is connected to P-101?')
    assert result['status'] == 'answered'
    assert result['evidence']
    assert 'V-201' in result['answer']
