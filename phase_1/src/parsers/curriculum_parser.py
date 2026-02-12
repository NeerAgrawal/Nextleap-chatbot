"""
Curriculum parser for extracting weekly course content.
"""
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict


class CurriculumParser:
    """Parse curriculum content from course page."""
    
    def __init__(self):
        self.weeks_pattern = re.compile(r'Week\s+(\d+):\s*([^\n]+)', re.IGNORECASE)
    
    def parse_from_html(self, html: str) -> Dict:
        """Parse curriculum from HTML content."""
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text(separator='\n', strip=False)
        
        return self.parse_from_text(text)
    
    def parse_from_text(self, text: str) -> Dict:
        """Parse curriculum from plain text."""
        weeks = []
        
        # Find all week headers
        week_matches = list(self.weeks_pattern.finditer(text))
        
        for i, match in enumerate(week_matches):
            week_number = int(match.group(1))
            week_title = match.group(2).strip()
            
            # Extract content between this week and the next
            start_pos = match.end()
            end_pos = week_matches[i + 1].start() if i + 1 < len(week_matches) else len(text)
            week_content = text[start_pos:end_pos].strip()
            
            # Parse week details
            week_data = self._parse_week_content(week_number, week_title, week_content)
            weeks.append(week_data)
        
        return {
            "total_weeks": len(weeks),
            "weeks": weeks
        }
    
    def _parse_week_content(self, week_number: int, title: str, content: str) -> Dict:
        """Parse individual week content."""
        lines = content.split('\n')
        
        topics = []
        hands_on = ""
        
        # Extract bullet points as topics
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '•', '*')):
                # Remove bullet and clean
                topic = re.sub(r'^[-•*]\s*', '', line).strip()
                if topic and len(topic) > 3:  # Avoid empty or very short lines
                    topics.append(topic)
            elif 'hands-on' in line.lower() or 'case on' in line.lower():
                hands_on = line.strip()
        
        return {
            "week_number": week_number,
            "title": title,
            "topics": topics,
            "hands_on_learning": hands_on,
            "content": content[:1000]  # First 1000 chars
        }
    
    def parse_from_file(self, file_path: str) -> Dict:
        """Parse curriculum from saved JSON or HTML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                data = json.load(f)
                text = data.get('full_text', '')
                return self.parse_from_text(text)
            else:  # HTML
                html = f.read()
                return self.parse_from_html(html)
    
    def save_to_json(self, curriculum_data: Dict, output_path: str) -> None:
        """Save parsed curriculum to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(curriculum_data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Saved curriculum data to {output_path}")


if __name__ == "__main__":
    parser = CurriculumParser()
    
    # Test with scraped data
    curriculum = parser.parse_from_file("data/raw/scraped_content.json")
    print(f"Parsed {curriculum['total_weeks']} weeks of curriculum")
    
    # Save
    parser.save_to_json(curriculum, "data/processed/curriculum.json")
