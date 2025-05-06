import os
import json
from typing import List, Dict, Any

# This is a simplified implementation of the memory layer
# In a production environment, you would use Supabase with pgvector as mentioned

class MemoryStore:
    def __init__(self, storage_path="./memory_data"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.memory_file = os.path.join(storage_path, "memories.json")
        self.load_memories()
    
    def load_memories(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                try:
                    self.memories = json.load(f)
                except json.JSONDecodeError:
                    self.memories = []
        else:
            self.memories = []
            self.save_memories()
    
    def save_memories(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def add_memory(self, content: str, metadata: Dict[str, Any] = None):
        """Add a new memory to the store"""
        memory = {
            "content": content,
            "metadata": metadata or {},
            "embedding": self._generate_simple_embedding(content)  # Placeholder for real embeddings
        }
        self.memories.append(memory)
        self.save_memories()
        return memory
    
    def _generate_simple_embedding(self, text: str) -> List[float]:
        """
        Placeholder for generating embeddings
        In a real implementation, you would use a proper embedding model
        """
        # This is just a dummy implementation
        import hashlib
        hash_val = hashlib.md5(text.encode()).hexdigest()
        # Convert hash to a list of 10 float values between -1 and 1
        return [(int(hash_val[i:i+2], 16) / 127.5) - 1 for i in range(0, 20, 2)]
    
    def retrieve_context(self, query: str, match_count: int = 5) -> str:
        """
        Retrieve relevant memories based on the query
        In a real implementation, this would use vector similarity search
        """
        # This is a simplified implementation
        # Sort memories by simple string matching (not vector similarity)
        query_lower = query.lower()
        scored_memories = []
        
        for memory in self.memories:
            # Simple scoring based on word overlap
            content_lower = memory["content"].lower()
            score = sum(1 for word in query_lower.split() if word in content_lower)
            scored_memories.append((score, memory))
        
        # Sort by score in descending order and take top match_count
        relevant_memories = [m[1]["content"] for m in sorted(scored_memories, key=lambda x: x[0], reverse=True)[:match_count]]
        
        return "\n".join(relevant_memories)