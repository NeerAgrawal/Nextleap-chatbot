"""
Improved instructor parser that works directly with HTML.
"""
import re
import sys
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.base_parser import BaseParser


class InstructorParser(BaseParser):
    """Parse instructor/mentor information from course HTML."""
    
    def parse(self, content: str) -> List[Dict]:
        """Parse all instructors from HTML content."""
        # First try HTML parsing
        instructors = self._parse_from_html(content)
        
        # If we got good results, return them
        if len(instructors) > 3:  # We should have at least 3-4 instructors
            return instructors
        
        # Fall back to text parsing if HTML parsing didn't work well
        return self._parse_from_text(content)
    
    def _parse_from_html(self, html: str) -> List[Dict]:
        """Extract instructors from HTML structure."""
        instructors = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Look for list items with instructor information
            # Pattern: <li><strong>Name</strong> description...</li>
            list_items = soup.find_all('li')
            
            for li in list_items:
                text = li.get_text(strip=True)
                
                # Check if this looks like an instructor entry
                # (contains teaching-related keywords)
                if any(keyword in text.lower()  for keyword in ['teaches', 'teaching', 'curriculum', 'module']):
                    instructor = self._extract_instructor_from_li(li, text)
                    if instructor:
                        instructors.append(instructor)
            
        except Exception as e:
            print(f"[INFO] HTML parsing encountered an issue: {e}")
        
        return self._deduplicate_by_name(instructors)
    
    def _extract_instructor_from_li(self, li_element, text: str) -> Dict:
        """Extract instructor details from a list item element."""
        # Try to find name in <strong> tag
        strong_tag = li_element.find('strong')
        name = strong_tag.get_text(strip=True) if strong_tag else None
        
        # If we found a name, extract other details
        if name and len(name) > 2 and len(name) < 50:
            # Extract full text
            full_text = text
            
            # Remove the name from text to get description
            description = full_text.replace(name, '', 1).strip()
            
            # Extract role/company
            role = self._extract_role(description)
            
            # Extract what they teach
            teaches = self._extract_teaching_info(description)
            
            # Extract background
            background = self._extract_background(description)
            
            return {
                "name": name,
                "title": role,
                "background": background,
                "teaches": teaches
            }
        
        return None
    
    def _extract_role(self, text: str) -> str:
        """Extract job title/role from description."""
        # Pattern 1: "is/was a/the [role] at [company]"
        role_patterns = [
            r'(?:is|was)\s+(?:a|the)\s+([^.]+?)\s+at\s+(\w+)',
            r'leads?\s+(?:the\s+)?([^.]+?)\s+at\s+(\w+)',
            r'([^.]*?(?:lead|manager|scientist|designer|engineer)[^.]*?)\s+at\s+(\w+)',
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                role_part = match.group(1).strip()
                company = match.group(2).strip()
                return f"{role_part} at {company}"
        
        return ""
    
    def _extract_teaching_info(self, text: str) -> str:
        """Extract what the instructor teaches."""
        # Pattern: "teaches [something]" or "teaching [something]"
        teaching_patterns = [
            r'teaches?\s+(?:the\s+)?([^.]+?)(?:\.|$)',
            r'teaching\s+(?:the\s+)?([^.]+?)(?:\.|$)',
        ]
        
        for pattern in teaching_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_background(self, text: str) -> str:
        """Extract background information."""
        # Look for "previously" or "was previously"
        bg_patterns = [
            r'(?:was\s+)?previously\s+([^.]+)',
            r'has\s+previously\s+worked\s+at\s+([^.]+)',
        ]
        
        for pattern in bg_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _parse_from_text(self, text: str) -> List[Dict]:
        """Fallback text-based parsing."""
        # Implement a simpler text-based parser as fallback
        return []
    
    def _deduplicate_by_name(self, instructors: List[Dict]) -> List[Dict]:
        """Remove duplicate instructors by name."""
        seen_names = set()
        unique = []
        
        for inst in instructors:
            name_normalized = inst['name'].lower().strip()
            if name_normalized not in seen_names:
                seen_names.add(name_normalized)
                unique.append(inst)
        
        return unique
    
    def parse_from_file(self, file_path: str) -> List[Dict]:
        """Parse instructors from file (HTML or JSON)."""
        # Load content
        content = ""
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Try to get HTML from JSON
                content = data.get('html', data.get('full_text', ''))
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        return self.parse(content)


if __name__ == "__main__":
    parser = InstructorParser()
    # Try parsing from the raw HTML file
    instructors = parser.parse_from_file("../../data/raw/course_page.html")
    print(f"Found {len(instructors)} instructors")
    for inst in instructors:
        print(f"  - {inst['name']}: {inst['teaches']}")
    parser.save_to_json(instructors, "../../data/processed/instructors.json")
