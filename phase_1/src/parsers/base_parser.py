"""
Base parser class with common functionality.
"""
import json
from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class for all parsers."""
    
    def __init__(self):
        self.data = {}
    
    @abstractmethod
    def parse(self, content: str) -> Dict[str, Any]:
        """Parse content and return structured data."""
        pass
    
    def load_from_file(self, file_path: str) -> str:
        """Load content from file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                data = json.load(f)
                return data.get('full_text', '')
            else:
                return f.read()
    
    def save_to_json(self, data: Dict, output_path: str) -> None:
        """Save parsed data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Saved data to {output_path}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        import re
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-:.,!?()&\n]', '', text)
        return text
