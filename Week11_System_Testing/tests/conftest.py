"""
Filename: tests/conftest.py
Provides lightweight test-only stubs so endpoint unit tests do not load
the real ChromaDB, SentenceTransformer, or spaCy models.
"""
import sys, types

class FakeEmbeddingModel:
    def __init__(self,*a,**k): pass
    def encode(self,text): return [0.0,0.0,0.0]

class FakeNLP:
    def __call__(self,text): return types.SimpleNamespace(ents=[])

class FakeCollection:
    def count(self): return 1
    def query(self,*a,**k):
        return {"ids":[[]],"documents":[[]],"metadatas":[[]],"distances":[[]]}

class FakeClient:
    def __init__(self,*a,**k): pass
    def get_collection(self,name): return FakeCollection()

m=types.ModuleType("sentence_transformers"); m.SentenceTransformer=FakeEmbeddingModel
sys.modules.setdefault("sentence_transformers",m)
m=types.ModuleType("spacy"); m.load=lambda *a,**k:FakeNLP()
sys.modules.setdefault("spacy",m)
m=types.ModuleType("chromadb"); m.PersistentClient=FakeClient
sys.modules.setdefault("chromadb",m)
