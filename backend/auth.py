import json
import uuid
from datetime import datetime
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.users_file = Path("../data/users.json")
        self.users_file.parent.mkdir(exist_ok=True)
        
        if not self.users_file.exists():
            self._initialize_users_file()
    
    def _initialize_users_file(self):
        """Initialize the users JSON file with sample data"""
        sample_users = {
            "students": [
                {
                    "id": "student_001",
                    "username": "john_math",
                    "name": "John",
                    "email": "john@example.com",
                    "registration_date": "2024-01-10T14:30:00",
                    "type": "student"
                },
                {
                    "id": "student_002",
                    "username": "sarah_geo",
                    "name": "Sarah",
                    "email": "sarah@example.com",
                    "registration_date": "2024-01-12T09:15:00",
                    "type": "student"
                }
            ],
            "guests": [],
            "sessions": []
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(sample_users, f, indent=2)
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {"students": [], "guests": [], "sessions": []}
    
    def save_users(self, users_data):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users_data, f, indent=2)
    
    def create_guest_user(self):
        """Create a new guest user"""
        users_data = self.load_users()
        
        guest_id = f"guest_{uuid.uuid4().hex[:8]}"
        guest_user = {
            "id": guest_id,
            "name": "Guest",
            "type": "guest",
            "created_at": datetime.now().isoformat()
        }
        
        users_data["guests"].append(guest_user)
        self.save_users(users_data)
        
        # Create session
        session = self.create_session(guest_id, "guest")
        
        return {
            "user_id": guest_id,
            "name": "Guest",
            "type": "guest",
            "session_id": session["session_id"]
        }
    
    def login_user(self, username):
        """Login a registered user"""
        users_data = self.load_users()
        
        # Check if user exists
        for student in users_data["students"]:
            if student["username"] == username or student["name"].lower() == username.lower():
                # Create session
                session = self.create_session(student["id"], "student")
                
                return {
                    "user_id": student["id"],
                    "name": student["name"],
                    "username": student["username"],
                    "type": "student",
                    "session_id": session["session_id"]
                }
        
        # Create new student
        student_id = f"student_{uuid.uuid4().hex[:8]}"
        new_student = {
            "id": student_id,
            "username": username.lower().replace(" ", "_"),
            "name": username,
            "registration_date": datetime.now().isoformat(),
            "type": "student"
        }
        
        users_data["students"].append(new_student)
        self.save_users(users_data)
        
        # Create session
        session = self.create_session(student_id, "student")
        
        return {
            "user_id": student_id,
            "name": username,
            "username": new_student["username"],
            "type": "student",
            "session_id": session["session_id"]
        }
    
    def create_session(self, user_id, user_type):
        """Create a new login session"""
        users_data = self.load_users()
        
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "user_type": user_type,
            "start_time": datetime.now().isoformat(),
            "is_active": True
        }
        
        users_data["sessions"].append(session)
        self.save_users(users_data)
        
        return session
    
    def end_session(self, session_id):
        """End a login session"""
        users_data = self.load_users()
        
        for session in users_data["sessions"]:
            if session["session_id"] == session_id:
                session["is_active"] = False
                session["end_time"] = datetime.now().isoformat()
                break
        
        self.save_users(users_data)
        return True