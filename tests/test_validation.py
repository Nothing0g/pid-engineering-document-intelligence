from pid_intel.config import DATA_PATH
from pid_intel.loader import DocumentStore
from pid_intel.validate import validate

def test_dangling_connection_is_blocked():
    store = DocumentStore(DATA_PATH)
    issues = validate(store.entities('rev-b'), store.connections('rev-b', include_validation_case=True))
    assert any(i.code == 'DANGLING_CONNECTION' and i.severity == 'error' for i in issues)
