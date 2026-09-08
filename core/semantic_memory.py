"""
Semantic Memory System
=====================
Vector-based memory using sentence embeddings.
Enables semantic search and context retrieval.
"""

import os
import json
import math
from datetime import datetime
from core.logger import logger


class SemanticMemory:
    def __init__(self):
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.vectors_file = os.path.join(self.memory_dir, "vectors.json")
        self.vectors = self._load()

        self._embedding_cache = {}
        self._use_tfidf = True

    def _load(self):
        if os.path.exists(self.vectors_file):
            try:
                with open(self.vectors_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"entries": [], "vocabulary": {}}

    def _save(self):
        with open(self.vectors_file, "w", encoding="utf-8") as f:
            json.dump(self.vectors, f, indent=2, ensure_ascii=False)

    def _tokenize(self, text):
        """Simple tokenization."""
        text = text.lower()
        for char in ".,!?;:'\"()-":
            text = text.replace(char, " ")
        return text.split()

    def _build_tfidf_vector(self, text):
        """Build TF-IDF-like vector from text."""
        tokens = self._tokenize(text)
        vocab = self.vectors.get("vocabulary", {})

        vector = {}
        for token in tokens:
            if token not in vocab:
                vocab[token] = len(vocab)
            idx = vocab[token]
            vector[idx] = vector.get(idx, 0) + 1

        self.vectors["vocabulary"] = vocab
        return vector

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2:
            return 0.0

        common_keys = set(vec1.keys()) & set(vec2.keys())
        if not common_keys:
            return 0.0

        dot_product = sum(vec1[k] * vec2[k] for k in common_keys)
        norm1 = math.sqrt(sum(v**2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v**2 for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def add(self, text, metadata=None):
        """Add an entry to semantic memory."""
        vector = self._build_tfidf_vector(text)

        entry = {
            "id": len(self.vectors["entries"]),
            "text": text,
            "vector": vector,
            "metadata": metadata or {},
            "created": datetime.now().isoformat()
        }

        self.vectors["entries"].append(entry)
        self._save()

        return entry["id"]

    def search(self, query, top_k=5, threshold=0.1):
        """Search semantic memory for similar entries."""
        query_vector = self._build_tfidf_vector(query)

        results = []
        for entry in self.vectors["entries"]:
            sim = self._cosine_similarity(query_vector, entry["vector"])
            if sim >= threshold:
                results.append({
                    "id": entry["id"],
                    "text": entry["text"],
                    "score": sim,
                    "metadata": entry["metadata"]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_context_string(self, query, top_k=3):
        """Get relevant context as a string for AI prompts."""
        results = self.search(query, top_k=top_k)
        if not results:
            return ""

        lines = ["Relevant memories:"]
        for r in results:
            lines.append(f"- {r['text']}")
        return "\n".join(lines)

    def delete(self, entry_id):
        """Delete an entry by ID."""
        self.vectors["entries"] = [e for e in self.vectors["entries"] if e["id"] != entry_id]
        self._save()

    def clear(self):
        """Clear all semantic memory."""
        self.vectors = {"entries": [], "vocabulary": {}}
        self._save()

    def get_stats(self):
        """Get memory statistics."""
        return {
            "entries": len(self.vectors["entries"]),
            "vocabulary_size": len(self.vectors.get("vocabulary", {}))
        }

    def learn_from_conversation(self, user_msg, response):
        """Automatically learn from conversations."""
        user_tokens = self._tokenize(user_msg)

        if len(user_tokens) > 3:
            self.add(user_msg, {"type": "conversation", "role": "user"})

        if len(self._tokenize(response)) > 3:
            self.add(response, {"type": "conversation", "role": "assistant"})
