from pid_intel.config import DATA_PATH
from pid_intel.loader import DocumentStore
from pid_intel.service import PidService

def test_revision_change_detects_instrument_replacement():
    result = PidService(DocumentStore(DATA_PATH)).compare('rev-a','rev-b')
    changes = result['entity_changes']
    assert changes['added'] == ['FT-101']
    assert changes['removed'] == ['PT-101']
    assert changes['changed_count'] == 2
