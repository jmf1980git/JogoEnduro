import json
import os
from datetime import datetime


class Database:
    MAX_RECORDS = 10  # Top 10 melhores

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

    def is_top_score(self, score):
        """Verifica se a pontuação entra no top 10."""
        if score <= 0:
            return False
        if len(self.records) < self.MAX_RECORDS:
            return True
        # Verifica se é maior que o menor score do top 10
        min_score = self.records[-1]['score'] if self.records else 0
        return score > min_score

    def add_record(self, name, score, level, difficulty):
        """Adiciona um record ao ranking (mantém apenas top 10)."""
        self.records.append({
            'name': name[:8],  # Máximo 8 caracteres
            'score': score,
            'level': level,
            'difficulty': difficulty,
            'date': datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        self.records.sort(key=lambda r: r['score'], reverse=True)
        self.records = self.records[:self.MAX_RECORDS]
        self._save()

    def get_top10(self):
        """Retorna os 10 melhores records."""
        return self.records[:self.MAX_RECORDS]

    def get_top5(self):
        """Retorna os 5 melhores records (compatibilidade)."""
        return self.records[:5]
