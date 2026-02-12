"""
Enhanced general parser for comprehensive program information.
"""
import re
import sys
from pathlib import Path
from typing import Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.base_parser import BaseParser
from utils.text_utils import (
    extract_money_amount, extract_duration, extract_date,
    extract_cohort_number, contains_keywords
)


class GeneralParser(BaseParser):
    """Parse general program information including schedule, cost, timeline."""
    
    def parse(self, content: str) -> Dict:
        """Parse all general program information."""
        return {
            "program_details": self._parse_program_details(content),
            "schedule": self._parse_schedule(content),
            "cost": self._parse_cost(content),
            "cohort_info": self._parse_cohort_info(content),
            "support": self._parse_support_info(content),
        }
    
    def _parse_program_details(self, text: str) -> Dict:
        """Extract program details like duration, hours, format."""
        details = {}
        
        # Extract hours (e.g., "100+ Hours")
        hours_match = re.search(r'(100\+?\s*(?:Hours?|hrs?))', text, re.IGNORECASE)
        if hours_match:
            details["total_hours"] = "100+ hours"
        else:
            # Fallback pattern
            hours_match = re.search(r'(\d+\+?)\s*(?:Hours?|hrs?)', text, re.IGNORECASE)
            if hours_match:
                details["total_hours"] = hours_match.group(0)
        
        # Extract fellowship duration (e.g., "4 months", "16 weeks")
        months_match = re.search(r'(\d+)\s*(?:months?|month)', text, re.IGNORECASE)
        if months_match:
            details["duration_months"] = f"{months_match.group(1)} months"
        
        weeks_match = re.search(r'(\d+)\s*(?:weeks?|week)', text, re.IGNORECASE)
        if weeks_match:
            details["duration_weeks"] = f"{weeks_match.group(1)} weeks"
        
        # Extract format
        if re.search(r'live\s+(?:online\s+)?class', text, re.IGNORECASE):
            details["format"] = "Live online classes"
        
        return details
    
    def _parse_schedule(self, text: str) -> Dict:
        """Parse class schedule with times and days."""
        schedule = {}
        
        # Look for time patterns (e.g., "10:30 AM - 12:30 PM IST")
        time_pattern = r'(\d{1,2}:\d{2}\s*(?:AM|PM))\s*-\s*(\d{1,2}:\d{2}\s*(?:AM|PM))\s*(?:IST)?'
        
        lines = text.split('\n')
        
        # Specific patterns for known schedule
        for i, line in enumerate(lines):
            time_match = re.search(time_pattern, line, re.IGNORECASE)
            if not time_match:
                continue
            
            time_slot = f"{time_match.group(1)} - {time_match.group(2)} IST"
            
            # Check context around this line for day information
            context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)]).lower()
            
            # Saturday sessions
            if 'saturday' in context:
                hour_start = int(time_match.group(1).split(':')[0])
                is_am = 'AM' in time_match.group(1).upper()
                
                if (hour_start == 10 and is_am) or (hour_start >=10 and hour_start <= 12 and is_am):
                    schedule["saturday_morning"] = time_slot
                elif hour_start >= 2 or 'PM' in time_match.group(1).upper():
                    schedule["saturday_afternoon"] = time_slot
            
            # Sunday sessions
            elif 'sunday' in context:
                if 'mentor' in context:
                    schedule["sunday_mentor_session"] = time_slot
                elif 'case' in context or 'hour' in context:
                    schedule["sunday_case_hours"] = time_slot
                else:
                    # Try to infer based on time
                    hour_start = int(time_match.group(1).split(':')[0])
                    is_am = 'AM' in time_match.group(1).upper()
                    if hour_start == 10 and is_am:
                        schedule["sunday_mentor_session"] = time_slot
                    elif hour_start >= 2:
                        schedule["sunday_case_hours"] = time_slot
            
            # Wednesday/Thursday sessions
            elif 'wednesday' in context or 'thursday' in context:
                if 'challenge' in context or 'product' in context:
                    schedule["wednesday_challenge"] = time_slot
            elif 'weekday' in context:
                schedule["weekday_session"] = time_slot
        
        return schedule
    
    def _parse_cost(self, text: str) -> Dict:
        """Extract cost information."""
        cost_info = {}
        
        # Extract price - look for specific amounts
        # Common patterns: ₹35,999 or 35999 or Rs 35999
        price_patterns = [
            r'[₹Rs]\s*35,?999',
            r'[₹Rs]\s*39,?999',
            r'[₹]\s?[\d,]+',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                cost_info["course_fee"] = match.group(0).strip()
                break
        
        return cost_info
    
    def _parse_cohort_info(self, text: str) -> Dict:
        """Extract cohort number and start date."""
        cohort_info = {}
        
        # Extract cohort number
        cohort_num = extract_cohort_number(text)
        if cohort_num:
            cohort_info["cohort_number"] = cohort_num
        
        # Extract start date - looking for specific date patterns
        date_patterns = [
            r'(?:starts?|starting|begins?)\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2}(?:,\s*\d{4})?)',
            r'([A-Z][a-z]+\s+\d{1,2}(?:,\s*\d{4})?)\s*(?:start|cohort)',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                cohort_info["start_date"] = match.group(1).strip()
                break
        
        return cohort_info
    
    def _parse_support_info(self, text: str) -> Dict:
        """Extract support and mentorship information."""
        support_info = {}
        
        # Mentorship - look for specific phrases
        mentor_patterns = [
            r'personalised mentorship from ([^.]+)',
            r'mentorship\s+(?:with\s+)?([^.\n]+?(?:PM|product manager|leader)[^.\n]*)',
            r'guidance.*from\s+([^.\n]+)',
        ]
        
        for pattern in mentor_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                support_info["mentorship"] = match.group(1).strip()
                break
        
        if not support_info.get("mentorship") and re.search(r'mentor', text, re.IGNORECASE):
            support_info["mentorship"] = "Experienced PMs from top companies"
        
        # Placement support
        placement_patterns = [
            r'placement support\s+for\s+(\d+\s+\w+)',
            r'(\d+\s+year)\s+placement',
        ]
        
        for pattern in placement_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                support_info["placement_support"] = match.group(1).strip() + " placement support"
                break
        
        if not support_info.get("placement_support") and re.search(r'placement.*support|job placement', text, re.IGNORECASE):
            support_info["placement_support"] = "1 year placement support"
        
        return support_info
    
    def parse_from_file(self, file_path: str) -> Dict:
        """Parse general info from file."""
        content = self.load_from_file(file_path)
        return self.parse(content)


if __name__ == "__main__":
    parser = GeneralParser()
    general_info = parser.parse_from_file("../../data/raw/scraped_content.json")
    print(f"Parsed general program information")
    parser.save_to_json(general_info, "../../data/processed/general_info.json")
