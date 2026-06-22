import json
import os
from datetime import datetime


class Database:
    def __init__(self):
        self.filename = 'records.json'
        self.records = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def add_record(self, name, score, level, difficulty):
        self.records.append({
            'name': name,
            'score': score,
            'level': level,
            'difficulty': difficulty,
            'date': datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        self.records.sort(key=lambda r: r['score'], reverse=True)
        self.records = self.records[:50]
        self._save()

    def get_top5(self):
        return self.records[:5]