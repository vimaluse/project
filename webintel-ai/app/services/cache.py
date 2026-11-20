import json, sqlite3, hashlib, time
from pathlib import Path
from app.config import settings

class AnalysisCache:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS analyses
                (cache_key TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at REAL NOT NULL)""")

    @staticmethod
    def key(url: str, text: str) -> str:
        return hashlib.sha256((url + "|" + text).encode()).hexdigest()

    def get(self, key: str):
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT payload, created_at FROM analyses WHERE cache_key=?", (key,)).fetchone()
        if not row or time.time() - row[1] > settings.cache_ttl_hours * 3600:
            return None
        return json.loads(row[0])

    def set(self, key: str, payload: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute("INSERT OR REPLACE INTO analyses VALUES (?, ?, ?)",
                         (key, json.dumps(payload), time.time()))
