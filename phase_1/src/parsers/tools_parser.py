"""
Tools parser for extracting tools and technologies.
"""
import re
import json
from typing import List, Dict


class ToolsParser:
    """Parse tools and technologies from course content."""
    
    def __init__(self):
        # Common tool categories
        self.categories = [
            "User Research", "Design", "Prototyping", "Data Analysis",
            "SQL", "AI Tools", "Collaboration", "Analytics", "Testing"
        ]
        
        # Common tools/technologies
        self.known_tools = [
            "Figma", "SQL", "GitHub", "Cursor", "Microsoft Clarity", "Hotjar",
            "Python", "ChatGPT", "Claude", "Groq", "API", "REST", "GraphQL",
            "MongoDB", "PostgreSQL", "ChromaDB", "FAISS", "LangChain"
        ]
    
    def parse_from_text(self, text: str) -> List[Dict]:
        """Parse tools from text content."""
        tools_by_category = {}
        
        lines = text.split('\n')
        current_category = "General"
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a category
            if any(cat.lower() in line.lower() for cat in self.categories):
                for cat in self.categories:
                    if cat.lower() in line.lower():
                        current_category = cat
                        break
            
            # Extract tools from line
            for tool in self.known_tools:
                if tool.lower() in line.lower():
                    if current_category not in tools_by_category:
                        tools_by_category[current_category] = set()
                    tools_by_category[current_category].add(tool)
        
        # Convert to list format
        tools_list = []
        for category, tools in tools_by_category.items():
            tools_list.append({
                "category": category,
                "tools": sorted(list(tools))
            })
        
        return tools_list
    
    def parse_from_file(self, file_path: str) -> List[Dict]:
        """Parse tools from saved JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = data.get('full_text', '')
        
        return self.parse_from_text(text)
    
    def save_to_json(self, tools: List[Dict], output_path: str) -> None:
        """Save parsed tools to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)
        
        total_tools = sum(len(cat['tools']) for cat in tools)
        print(f"[OK] Saved {total_tools} tools across {len(tools)} categories to {output_path}")


if __name__ == "__main__":
    parser = ToolsParser()
    
    # Test with scraped data
    tools = parser.parse_from_file("data/raw/scraped_content.json")
    print(f"Parsed tools from {len(tools)} categories")
    
    # Save
    parser.save_to_json(tools, "data/processed/tools.json")
