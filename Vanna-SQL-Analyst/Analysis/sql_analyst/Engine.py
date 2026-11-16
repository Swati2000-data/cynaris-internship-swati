
from pathlib import Path

from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore


class LocalVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "database" / "retail.db"


def get_vanna():
    vn = LocalVanna(
        config={
            "model": "qwen2.5:3b",
            "path": str(PROJECT_ROOT / "chroma_db")
        }
    )

    vn.connect_to_sqlite(str(DATABASE_PATH))
    return vn
