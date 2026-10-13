from fastapi import FastAPI, HTTPException, Query
from .config import DATA_PATH
from .loader import DocumentStore
from .service import PidService

app = FastAPI(title="P&ID Engineering-Document Intelligence", version="0.1.0")
service = PidService(DocumentStore(DATA_PATH))

@app.get('/health')
def health():
    return {'status':'ok','service':'pid-engineering-document-intelligence'}

@app.get('/documents/{revision}/extract')
def extract(revision: str):
    try: return service.extract(revision)
    except KeyError: raise HTTPException(404, 'revision not found')

@app.get('/documents/compare')
def compare(base: str = Query(...), candidate: str = Query(...)):
    try: return service.compare(base, candidate)
    except KeyError: raise HTTPException(404, 'revision not found')

@app.get('/documents/{revision}/ask')
def ask(revision: str, q: str = Query(..., min_length=3)):
    try: return service.ask(revision, q)
    except KeyError: raise HTTPException(404, 'revision not found')
