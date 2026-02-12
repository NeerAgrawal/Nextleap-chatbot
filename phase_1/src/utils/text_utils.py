"""
Utility functions for text processing and pattern matching.
"""
import re
from typing import List, Optional


def extract_name_from_text(text: str) -> Optional[str]:
    """
    Extract person name from text.
    Names are usually capitalized words at the start of a paragraph.
    """
    lines = text.split('\n')
    for line in lines[:3]:  # Check first 3 lines
        # Look for capitalized words (2-4 words max for name)
        name_pattern = r'^([A-Z][a-z]+(?: [A-Z][a-z]+){0,3})\b'
        match = re.search(name_pattern, line.strip())
        if match:
            potential_name = match.group(1)
            # Filter out common false positives
            if len(potential_name.split()) >= 2 and len(potential_name) < 50:
                return potential_name
    return None


def extract_money_amount(text: str) -> Optional[str]:
    """Extract money amounts like ₹35,999 or $500."""
    pattern = r'[₹$]\s?[\d,]+'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_duration(text: str) -> Optional[str]:
    """Extract duration like '4 months', '100+ hours', '16 weeks'."""
    patterns = [
        r'\d+\+?\s*(?:hours?|hrs?)',
        r'\d+\s*(?:months?|weeks?|days?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def extract_date(text: str) -> Optional[str]:
    """Extract dates like 'Mar 7', 'March 7, 2024'."""
    patterns = [
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:,\s*\d{4})?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def extract_cohort_number(text: str) -> Optional[int]:
    """Extract cohort number like 'Cohort 47'."""
    match = re.search(r'Cohort\s+(\d+)', text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def split_into_sections(text: str, separator_pattern: str = r'\n\n+') -> List[str]:
    """Split text into sections based on separator pattern."""
    return [s.strip() for s in re.split(separator_pattern, text) if s.strip()]


def contains_keywords(text: str, keywords: List[str], case_sensitive: bool = False) -> bool:
    """Check if text contains any of the keywords."""
    if not case_sensitive:
        text = text.lower()
        keywords = [k.lower() for k in keywords]
    
    return any(keyword in text for keyword in keywords)
