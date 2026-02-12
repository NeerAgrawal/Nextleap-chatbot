# Phase 1: Data Collection & Preprocessing

This folder contains all Phase 1 implementation for web scraping and data processing.

## Structure

```
phase_1/
├── src/
│   ├── scrapers/          # Web scraping modules
│   ├── parsers/           # Content parsing (modular)
│   │   ├── base_parser.py       # Base class for all parsers
│   │   ├── instructor_parser.py # Extract all instructors
│   │   ├── general_parser.py    # Extract program details
│   │   ├── curriculum_parser.py # Extract 13 weeks
│   │   └── tools_parser.py      # Extract tools
│   └── utils/             # Helper utilities
│       └── text_utils.py  # Text extraction functions
├── data/
│   ├── raw/              # Raw scraped HTML/JSON
│   ├── processed/        # Structured output
│   └── metadata/         # Scraping logs
├── config/
│   └── config.yaml       # Configuration
└── scripts/
    └── run_phase1.py     # Main execution script
```

## Running Phase 1

```bash
cd phase_1
python scripts/run_phase1.py
```

## Modular Architecture

- **BaseParser**: Abstract base class with common functionality
- **text_utils**: Reusable text extraction functions
- **Improved parsers**: Enhanced extraction for instructors and program details

## Output Data

- **curriculum.json**: 13 weeks of course content
- **instructors.json**: All instructor/mentor profiles
- **tools.json**: Tools categorized by type
- **general_info.json**: Program details (hours, timeline, cost, cohort, support)
