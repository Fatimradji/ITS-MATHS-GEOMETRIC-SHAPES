import json
from datetime import datetime
from pathlib import Path

class ProgressManager:
    def __init__(self):
        self.progress_file = Path("../data/progress.json")
        self.progress_file.parent.mkdir(exist_ok=True)
        
        if not self.progress_file.exists():
            self._initialize_progress_file()
    
    def _initialize_progress_file(self):
        """Initialize the progress JSON file"""
        sample_progress = {
            "john_math": {
                "user_id": "student_001",
                "name": "John",
                "quiz": {
                    "total_score": 85,
                    "total_quizzes": 2,
                    "average_score": 85,
                    "last_quiz": "2024-01-15T10:45:00"
                },
                "practice": {
                    "completed_exercises": 8,
                    "correct_answers": 7,
                    "accuracy": 87.5,
                    "last_practice": "2024-01-15T10:30:00"
                },
                "overall_progress": 86.25,
                "learning_patterns": {
                    "strong_areas": ["cube_volume", "triangle_area"],
                    "weak_areas": ["sphere_surface", "cylinder_volume"],
                    "last_activity": "2024-01-15T10:45:00"
                }
            }
        }
        
        with open(self.progress_file, 'w') as f:
            json.dump(sample_progress, f, indent=2)
    
    def load_progress(self):
        """Load progress data from JSON file"""
        try:
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_progress_data(self, progress_data):
        """Save progress data to JSON file"""
        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
    
    def get_progress(self, user_id):
        """Get progress for a specific user"""
        progress_data = self.load_progress()
        return progress_data.get(user_id, self._create_default_progress(user_id))
    
    def _create_default_progress(self, user_id):
        """Create default progress structure for a new user"""
        return {
            "user_id": user_id,
            "quiz": {
                "total_score": 0,
                "total_quizzes": 0,
                "average_score": 0,
                "last_quiz": None
            },
            "practice": {
                "completed_exercises": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "last_practice": None
            },
            "overall_progress": 0,
            "learning_patterns": {
                "strong_areas": [],
                "weak_areas": [],
                "last_activity": None
            }
        }
    
    def save_progress(self, user_id, progress_update):
        """Save progress update for a user"""
        progress_data = self.load_progress()
        
        if user_id not in progress_data:
            progress_data[user_id] = self._create_default_progress(user_id)
        
        # Update quiz progress
        if "quiz" in progress_update:
            quiz_data = progress_update["quiz"]
            current_quiz = progress_data[user_id]["quiz"]
            
            if "score" in quiz_data and "total" in quiz_data:
                current_quiz["total_score"] += quiz_data["score"]
                current_quiz["total_quizzes"] += 1
                current_quiz["average_score"] = current_quiz["total_score"] / current_quiz["total_quizzes"]
                current_quiz["last_quiz"] = datetime.now().isoformat()
        
        # Update practice progress
        if "practice" in progress_update:
            practice_data = progress_update["practice"]
            current_practice = progress_data[user_id]["practice"]
            
            if "completed" in practice_data:
                current_practice["completed_exercises"] += len(practice_data["completed"])
            
            if "correct" in practice_data:
                current_practice["correct_answers"] += practice_data["correct"]
            
            if current_practice["completed_exercises"] > 0:
                current_practice["accuracy"] = (current_practice["correct_answers"] / current_practice["completed_exercises"]) * 100
            
            current_practice["last_practice"] = datetime.now().isoformat()
        
        # Update overall progress
        quiz_avg = progress_data[user_id]["quiz"]["average_score"]
        practice_acc = progress_data[user_id]["practice"]["accuracy"]
        
        if quiz_avg > 0 and practice_acc > 0:
            progress_data[user_id]["overall_progress"] = (quiz_avg + practice_acc) / 2
        elif quiz_avg > 0:
            progress_data[user_id]["overall_progress"] = quiz_avg
        elif practice_acc > 0:
            progress_data[user_id]["overall_progress"] = practice_acc
        
        # Update last activity
        progress_data[user_id]["learning_patterns"]["last_activity"] = datetime.now().isoformat()
        
        self.save_progress_data(progress_data)
        return True
    
    def save_quiz_result(self, user_id, quiz_result):
        """Save quiz result for a user"""
        progress_update = {
            "quiz": {
                "score": quiz_result.get("score", 0),
                "total": quiz_result.get("total", 1)
            }
        }
        return self.save_progress(user_id, progress_update)
    
    def save_practice_result(self, user_id, practice_result):
        """Save practice result for a user"""
        progress_update = {
            "practice": {
                "completed": practice_result.get("completed_exercises", []),
                "correct": practice_result.get("correct_answers", 0)
            }
        }
        return self.save_progress(user_id, progress_update)
    
    def update_learning_pattern(self, user_id, topic):
        """Update learning patterns based on user interactions"""
        progress_data = self.load_progress()
        
        if user_id not in progress_data:
            progress_data[user_id] = self._create_default_progress(user_id)
        
        # Simple pattern tracking - in a real system this would be more sophisticated
        patterns = progress_data[user_id]["learning_patterns"]
        
        # Extract shape from topic
        shapes = ["cube", "sphere", "cone", "cylinder", "triangle", "rectangle"]
        for shape in shapes:
            if shape in topic.lower():
                if shape not in patterns["strong_areas"] and shape not in patterns["weak_areas"]:
                    # Add to weak areas initially (needs more practice)
                    patterns["weak_areas"].append(shape)
                break
        
        patterns["last_activity"] = datetime.now().isoformat()
        
        self.save_progress_data(progress_data)
        return True