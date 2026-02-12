"""
Main script to run Phase 1: Data scraping and preprocessing.
Updated version with modular architecture.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scrapers.course_scraper import CoursePageScraper
from parsers.curriculum_parser import CurriculumParser
from parsers.instructor_parser import InstructorParser
from parsers.tools_parser import ToolsParser
from parsers.general_parser import GeneralParser


def main():
    """Execute Phase 1 pipeline with improved parsers."""
    print("\n" + "="*70)
    print(" PHASE 1: DATA COLLECTION & PREPROCESSING (Modular Version)")
    print("="*70 + "\n")
    
    metadata = {
        "phase": "Phase 1",
        "started_at": datetime.now().isoformat(),
        "steps": []
    }
    
    # Step 1: Scrape course page
    print("Step 1: Scraping course page...")
    print("-" * 70)
    scraper = CoursePageScraper()
    scraper.course_url = "https://nextleap.app/course/product-management-course"
    scraper.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Fetch HTML
    html = scraper.fetch_page()
    if not html:
        print("[X] Scraping failed")
        return
    
    # Save raw data
    scraper.save_raw_html(html, output_dir="data/raw")
    data = scraper.extract_initial_data(html)
    scraper.save_initial_json(data, output_dir="data/raw")
    
    metadata['steps'].append({
        "step": "scraping",
        "status": "success",
    })
    print()
    
    # Step 2: Parse curriculum
    print("Step 2: Parsing curriculum...")
    print("-" * 70)
    curriculum_parser = CurriculumParser()
    curriculum = curriculum_parser.parse_from_file("data/raw/scraped_content.json")
    curriculum_parser.save_to_json(curriculum, "data/processed/curriculum.json")
    
    metadata['steps'].append({
        "step": "curriculum_parsing",
        "status": "success",
        "weeks_found": curriculum['total_weeks']
    })
    print()
    
    # Step 3: Parse instructors (IMPROVED - using HTML)
    print("Step 3: Parsing instructors (improved - from HTML)...")
    print("-" * 70)
    instructor_parser = InstructorParser()
    instructors = instructor_parser.parse_from_file("data/raw/course_page.html")
    instructor_parser.save_to_json(instructors, "data/processed/instructors.json")
    
    print(f"[INFO] Found {len(instructors)} instructors:")
    for inst in instructors:
        print(f"  - {inst['name']}: {inst.get('teaches', 'N/A')}")
    
    metadata['steps'].append({
        "step": "instructor_parsing",
        "status": "success",
        "instructors_found": len(instructors)
    })
    print()
    
    # Step 4: Parse tools
    print("Step 4: Parsing tools and technologies...")
    print("-" * 70)
    tools_parser = ToolsParser()
    tools = tools_parser.parse_from_file("data/raw/scraped_content.json")
    tools_parser.save_to_json(tools, "data/processed/tools.json")
    
    metadata['steps'].append({
        "step": "tools_parsing",
        "status": "success",
        "categories_found": len(tools)
    })
    print()
    
    # Step 5: Parse general information (ENHANCED)
    print("Step 5: Parsing comprehensive program information...")
    print("-" * 70)
    general_parser = GeneralParser()
    general_info = general_parser.parse_from_file("data/raw/scraped_content.json")
    general_parser.save_to_json(general_info, "data/processed/general_info.json")
    
    # Display extracted info
    print("[INFO] Program details extracted:")
    if 'program_details' in general_info:
        for key, value in general_info['program_details'].items():
            print(f"  - {key}: {value}")
    if 'cost' in general_info and general_info['cost']:
        course_fee = general_info['cost'].get('course_fee', 'N/A')
        # Replace rupee symbol with ASCII for Windows console
        if course_fee != 'N/A':
            course_fee = course_fee.replace('₹', 'Rs ')
        print(f"  - Course fee: {course_fee}")
    if 'cohort_info' in general_info and general_info['cohort_info']:
        for key, value in general_info['cohort_info'].items():
            print(f"  - {key}: {value}")
    
    metadata['steps'].append({
        "step": "general_parsing",
        "status": "success",
    })
    print()
    
    # Save metadata
    metadata['completed_at'] = datetime.now().isoformat()
    metadata['status'] = 'success'
    
    metadata_path = Path("data/metadata/phase1_log.json")
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print(" PHASE 1 COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\n[SUMMARY]:")
    print(f"  * Weeks of curriculum: {curriculum['total_weeks']}")
    print(f"  * Instructors found: {len(instructors)}")
    print(f"  * Tool categories: {len(tools)}")
    print(f"\n[OUTPUT FILES]:")
    print(f"  * phase_1/data/processed/curriculum.json")
    print(f"  * phase_1/data/processed/instructors.json")
    print(f"  * phase_1/data/processed/tools.json")
    print(f"  * phase_1/data/processed/general_info.json")
    print(f"  * phase_1/data/metadata/phase1_log.json")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
