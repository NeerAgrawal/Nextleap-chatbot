"""
Course scraper for Nextleap Product Management Fellowship page.
"""
import requests
import json
import time
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, Optional
import yaml
import os


class CoursePageScraper:
    """Scraper for Nextleap course page."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize scraper with optional configuration.
        
        Args:
            config_path: Path to YAML config file (optional)
        """
        # Set default values
        self.course_url = "https://nextleap.app/course/product-management-course"
        self.timeout = 30
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Load config if provided and exists
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            scraping_config = config.get('scraping', {})
            self.course_url = scraping_config.get('course_url', self.course_url)
            self.timeout = scraping_config.get('timeout_seconds', self.timeout)
            self.user_agent = scraping_config.get('user_agent', self.user_agent)
        
        # Construct headers after user_agent is finalized
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def fetch_page(self) -> Optional[str]:
        """Fetch the course page HTML."""
        print(f"Fetching course page from {self.course_url}...")
        
        try:
            response = requests.get(
                self.course_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            print(f"[OK] Successfully fetched page (Status: {response.status_code})")
            return response.text
        
        except requests.exceptions.RequestException as e:
            print(f"[X] Error fetching page: {e}")
            return None
    
    def save_raw_html(self, html: str, output_dir: str = "data/raw") -> str:
        """Save raw HTML to file."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        output_path = Path(output_dir) / "course_page.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[OK] Saved raw HTML to {output_path}")
        return str(output_path)
    
    def extract_initial_data(self, html: str) -> Dict:
        """Extract initial structured data from HTML."""
        soup = BeautifulSoup(html, 'lxml')
        
        data = {
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "url": self.course_url,
                "title": soup.find('title').text if soup.find('title') else "Unknown"
            },
            "raw_sections": {}
        }
        
        # Extract main sections
        sections = soup.find_all(['section', 'div'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['curriculum', 'instructor', 'tool', 'schedule', 'testimonial']
        ))
        
        for i, section in enumerate(sections):
            section_id = section.get('id', f'section_{i}')
            data["raw_sections"][section_id] = {
                "html": str(section),
                "text": section.get_text(strip=True)[:500]  # First 500 chars as preview
            }
        
        # Extract all text content for fallback
        data["full_text"] = soup.get_text(separator='\n', strip=True)
        
        return data
    
    def save_initial_json(self, data: Dict, output_dir: str = "data/raw") -> str:
        """Save initial extracted data as JSON."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        output_path = Path(output_dir) / "scraped_content.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Saved initial data to {output_path}")
        return str(output_path)
    
    def scrape(self) -> Dict[str, str]:
        """
        Main scraping method.
        Returns dict with paths to saved files.
        """
        print("\n" + "="*60)
        print("Starting Nextleap Course Page Scraping")
        print("="*60 + "\n")
        
        # Fetch HTML
        html = self.fetch_page()
        if not html:
            return {"status": "failed", "error": "Could not fetch page"}
        
        # Save raw HTML
        html_path = self.save_raw_html(html)
        
        # Extract initial data
        data = self.extract_initial_data(html)
        
        # Save JSON
        json_path = self.save_initial_json(data)
        
        print("\n" + "="*60)
        print("Scraping completed successfully!")
        print("="*60 + "\n")
        
        return {
            "status": "success",
            "html_path": html_path,
            "json_path": json_path,
            "metadata": data["metadata"]
        }


if __name__ == "__main__":
    scraper = CoursePageScraper()
    result = scraper.scrape()
    print(f"\nResult: {json.dumps(result, indent=2)}")
