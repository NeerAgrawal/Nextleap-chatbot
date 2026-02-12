"""
Text chunker for Phase 2: Convert Phase 1 processed data into semantic chunks for embedding.
"""
import json
from pathlib import Path
from typing import List, Dict


class TextChunker:
    """Chunk processed data into semantic units for embedding."""
    
    def __init__(self):
        self.chunks = []
        self.chunk_counter = 0
    
    def load_phase1_data(self, phase1_dir: str) -> Dict:
        """Load all Phase 1 processed data."""
        phase1_path = Path(phase1_dir)
        
        data = {}
        data['curriculum'] = self._load_json(phase1_path / 'curriculum.json')
        data['instructors'] = self._load_json(phase1_path / 'instructors.json')
        data['tools'] = self._load_json(phase1_path / 'tools.json')
        data['general_info'] = self._load_json(phase1_path / 'general_info.json')
        
        return data
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def chunk_curriculum(self, curriculum_data: Dict) -> List[Dict]:
        """Chunk curriculum data by week."""
        chunks = []
        
        for week in curriculum_data.get('weeks', []):
            chunk_id = f"curr_week{week['week_number']:02d}"
            
            # Build rich content for the week
            content_parts = [
                f"Week {week['week_number']}: {week['title']}",
                "",
                f"Content: {week['content']}",
            ]
            
            if week.get('hands_on_learning'):
                content_parts.append(f"\nHands-on Learning: {week['hands_on_learning']}")
            
            content = "\n".join(content_parts)
            
            chunk = {
                "chunk_id": chunk_id,
                "content": content,
                "metadata": {
                    "source": "phase1_curriculum",
                    "category": "curriculum",
                    "week": week['week_number'],
                    "title": week['title'],
                    "chunk_type": "weekly_content"
                }
            }
            chunks.append(chunk)
        
        return chunks
    
    def chunk_instructors(self, instructors_data: List[Dict]) -> List[Dict]:
        """Chunk instructor data - one chunk per instructor."""
        chunks = []
        
        for idx, instructor in enumerate(instructors_data):
            chunk_id = f"inst_{idx+1:02d}_{instructor['name'].lower().replace(' ', '_')}"
            
            # Build instructor profile
            content_parts = [
                f"Instructor: {instructor['name']}",
                f"Title: {instructor['title']}",
            ]
            
            if instructor.get('background'):
                content_parts.append(f"Background: {instructor['background']}")
            
            if instructor.get('teaches'):
                content_parts.append(f"Teaches: {instructor['teaches']}")
            
            content = "\n".join(content_parts)
            
            chunk = {
                "chunk_id": chunk_id,
                "content": content,
                "metadata": {
                    "source": "phase1_instructors",
                    "category": "instructors",
                    "instructor_name": instructor['name'],
                    "chunk_type": "instructor_profile"
                }
            }
            chunks.append(chunk)
        
        return chunks
    
    def chunk_tools(self, tools_data: List[Dict]) -> List[Dict]:
        """Chunk tools data by category."""
        chunks = []
        
        for idx, tool_category in enumerate(tools_data):
            category_name = tool_category.get('category', f'category_{idx}')
            chunk_id = f"tools_{category_name.lower().replace(' ', '_').replace('&', 'and')}"
            
            tools_list = tool_category.get('tools', [])
            tools_str = ", ".join(tools_list) if tools_list else "Various tools"
            
            content = f"Tools Category: {category_name}\nTools: {tools_str}"
            
            if tool_category.get('description'):
                content += f"\nDescription: {tool_category['description']}"
            
            chunk = {
                "chunk_id": chunk_id,
                "content": content,
                "metadata": {
                    "source": "phase1_tools",
                    "category": "tools",
                    "tool_category": category_name,
                    "chunk_type": "tools_category"
                }
            }
            chunks.append(chunk)
        
        return chunks
    
    def chunk_general_info(self, general_data: Dict) -> List[Dict]:
        """Chunk general program information."""
        chunks = []
        
        # Chunk 1: Program Details
        if 'program_details' in general_data:
            details = general_data['program_details']
            content_parts = ["Program Details:"]
            
            if details.get('course_name'):
                content_parts.append(f"Course Name: {details['course_name']}")
            if details.get('provider'):
                content_parts.append(f"Provider: {details['provider']}")
            if details.get('total_hours'):
                content_parts.append(f"Duration: {details['total_hours']}")
            if details.get('duration_months'):
                content_parts.append(f"Timeline: {details['duration_months']}")
            if details.get('duration_weeks'):
                content_parts.append(f"Weeks: {details['duration_weeks']}")
            if details.get('format'):
                content_parts.append(f"Format: {details['format']}")
            
            chunk = {
                "chunk_id": "general_program_details",
                "content": "\n".join(content_parts),
                "metadata": {
                    "source": "phase1_general_info",
                    "category": "general",
                    "chunk_type": "program_details"
                }
            }
            chunks.append(chunk)
        
        # Chunk 2: Schedule
        if 'schedule' in general_data:
            schedule = general_data['schedule']
            content_parts = ["Class Schedule:"]
            
            if schedule.get('saturday_morning'):
                content_parts.append(f"Saturday Morning: {schedule['saturday_morning']}")
            if schedule.get('saturday_afternoon'):
                content_parts.append(f"Saturday Afternoon: {schedule['saturday_afternoon']}")
            if schedule.get('sunday_mentor_session'):
                content_parts.append(f"Sunday Mentor Session: {schedule['sunday_mentor_session']}")
            if schedule.get('sunday_case_hours'):
                content_parts.append(f"Sunday Case Hours: {schedule['sunday_case_hours']}")
            if schedule.get('wednesday_challenge'):
                content_parts.append(f"Wednesday Product Challenge: {schedule['wednesday_challenge']}")
            
            chunk = {
                "chunk_id": "general_schedule",
                "content": "\n".join(content_parts),
                "metadata": {
                    "source": "phase1_general_info",
                    "category": "general",
                    "chunk_type": "schedule"
                }
            }
            chunks.append(chunk)
        
        # Chunk 3: Cost
        if 'cost' in general_data:
            cost = general_data['cost']
            content = f"Course Fee: {cost.get('course_fee', 'N/A')}"
            
            chunk = {
                "chunk_id": "general_cost",
                "content": content,
                "metadata": {
                    "source": "phase1_general_info",
                    "category": "general",
                    "chunk_type": "cost"
                }
            }
            chunks.append(chunk)
        
        # Chunk 4: Cohort Info
        if 'cohort' in general_data:
            cohort = general_data['cohort']
            content_parts = ["Cohort Information:"]
            
            if cohort.get('cohort_number'):
                content_parts.append(f"Cohort Number: {cohort['cohort_number']}")
            if cohort.get('start_date'):
                content_parts.append(f"Start Date: {cohort['start_date']}")
            
            chunk = {
                "chunk_id": "general_cohort",
                "content": "\n".join(content_parts),
                "metadata": {
                    "source": "phase1_general_info",
                    "category": "general",
                    "chunk_type": "cohort"
                }
            }
            chunks.append(chunk)
        
        # Chunk 5: Support
        if 'support' in general_data:
            support = general_data['support']
            content_parts = ["Support Services:"]
            
            if support.get('mentorship'):
                content_parts.append(f"Mentorship: {support['mentorship']}")
            if support.get('placement_support'):
                content_parts.append(f"Placement Support: {support['placement_support']}")
            
            chunk = {
                "chunk_id": "general_support",
                "content": "\n".join(content_parts),
                "metadata": {
                    "source": "phase1_general_info",
                    "category": "general",
                    "chunk_type": "support"
                }
            }
            chunks.append(chunk)
        
        return chunks
    
    def create_all_chunks(self, phase1_data: Dict) -> List[Dict]:
        """Create all chunks from Phase 1 data."""
        all_chunks = []
        
        # Chunk curriculum
        curr_chunks = self.chunk_curriculum(phase1_data['curriculum'])
        all_chunks.extend(curr_chunks)
        print(f"[INFO] Created {len(curr_chunks)} curriculum chunks")
        
        # Chunk instructors
        inst_chunks = self.chunk_instructors(phase1_data['instructors'])
        all_chunks.extend(inst_chunks)
        print(f"[INFO] Created {len(inst_chunks)} instructor chunks")
        
        # Chunk tools
        tool_chunks = self.chunk_tools(phase1_data['tools'])
        all_chunks.extend(tool_chunks)
        print(f"[INFO] Created {len(tool_chunks)} tool chunks")
        
        # Chunk general info
        gen_chunks = self.chunk_general_info(phase1_data['general_info'])
        all_chunks.extend(gen_chunks)
        print(f"[INFO] Created {len(gen_chunks)} general info chunks")
        
        print(f"\n[SUCCESS] Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    def save_chunks(self, chunks: List[Dict], output_path: str):
        """Save chunks to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Saved {len(chunks)} chunks to {output_path}")


if __name__ == "__main__":
    # Test chunker
    chunker = TextChunker()
    data = chunker.load_phase1_data("../../phase_1/data/processed")
    chunks = chunker.create_all_chunks(data)
    chunker.save_chunks(chunks, "../data/chunks/all_chunks.json")
