import sys
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from collections import defaultdict  # Added import

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Add both current dir and project root to Python path
sys.path.insert(0, current_dir)  # Add backend directory
sys.path.insert(0, project_root)  # Add project root

print(f" Debug: Current directory: {current_dir}")
print(f"Debug: Project root: {project_root}")
print(f" Debug: Python path: {sys.path}")

# First check if we can import auth directly
print("\n Testing imports...")

# Try to import auth module with different approaches
auth_module = None
progress_module = None
tutor_module = None
ontology_loader = None

# Method 1: direct file import for auth
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("auth", os.path.join(current_dir, "auth.py"))
    auth_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(auth_module)
    print("Method 1: auth imported via file path")
except Exception as e:
    print(f"Method 1 failed: {e}")

# import ontology loader
try:
    from ontology.ontology_loader import OntologyLoader
    ontology_path = os.path.join(project_root, "ontology", "my_ontologyIts.xml")
    print(f" OntologyLoader imported, loading from: {ontology_path}")
    
    if os.path.exists(ontology_path):
        ontology_loader = OntologyLoader(ontology_path)
        if ontology_loader.load_ontology():
            print("Ontology loaded successfully!")
        else:
            print("Ontology loading failed")
    else:
        print(f" Ontology file not found at: {ontology_path}")
        ontology_loader = None
except ImportError as e:
    print(f" OntologyLoader import failed: {e}")
    ontology_loader = None
except Exception as e:
    print(f" Ontology error: {e}")
    ontology_loader = None

# Create the Flask app
app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')
CORS(app)

# If auth_module was imported successfully, use it
if auth_module:
    auth_manager = auth_module.AuthManager()
    print(" AuthManager created successfully")
else:
    # Create a dummy AuthManager
    print(" Creating dummy AuthManager")
    class AuthManager:
        def create_guest_user(self):
            return {"user_id": "guest_001", "name": "Guest", "type": "guest"}
        def login_user(self, username):
            return {"user_id": f"student_{username}", "name": username, "type": "student"}
    auth_manager = AuthManager()

# Create progress manager use ontology data
class ProgressManager:
    def __init__(self):
        self.ontology_loader = ontology_loader
    
    def save_progress(self, user_id, progress):
        print(f" Saving progress for {user_id}: {progress}")
        return True
    
    def get_progress(self, user_id):
        # get progress from ontology 
        if self.ontology_loader and hasattr(self.ontology_loader, 'get_progress_data'):
            try:
                progress_data = self.ontology_loader.get_progress_data()
                for progress in progress_data:
                    # Check  progress for the user
                    if user_id in progress.get('name', '') or user_id in progress.get('uri', ''):
                        return {
                            "quiz_score": int(progress.get('metrics', {}).get('quiz_score', 0)),
                            "practice_score": int(progress.get('metrics', {}).get('practice_score', 0)),
                            "completion_percentage": float(progress.get('metrics', {}).get('completion_percentage', 0)),
                            "from_ontology": True
                        }
            except Exception as e:
                print(f"Error getting progress from ontology: {e}")
        
        # Fallback to default
        return {"quiz_score": 0, "practice_score": 0, "overall": 0, "from_ontology": False}

# Create AI Tutor from ontology data
class AITutor:
    def __init__(self):
        self.name = "AI Tutor"
        self.specialization = "Geometry"
        self.from_ontology = False
        
        # get AI Tutor from ontology
        if ontology_loader and hasattr(ontology_loader, 'get_ai_tutor'):
            try:
                ontology_tutor = ontology_loader.get_ai_tutor()
                if ontology_tutor:
                    self.name = ontology_tutor.get('name', self.name)
                    self.specialization = ontology_tutor.get('specialization', self.specialization)
                    self.from_ontology = True
                    print(f" Using AI Tutor from ontology: {self.name}")
                else:
                    print(" No AI Tutor found in ontology, using default")
            except Exception as e:
                print(f"Error getting AI Tutor from ontology: {e}")
        
        self.responses = {
            "hello": f"Hello! I'm {self.name}, your {self.specialization} tutor. How can I help?",
            "cube": "A cube has 6 faces. Volume = a³, Surface Area = 6a²",
            "sphere": "A sphere is round. Volume = 4/3 π r³, Surface Area = 4πr²",
            "cone": "A cone has a circular base. Volume = (1/3) π r² h",
            "cylinder": "A cylinder has two circular bases. Volume = π r² h",
            "triangle": "A triangle has 3 sides. Area = 1/2 × base × height",
            "rectangle": "A rectangle has 4 sides. Area = length × width",
            "hi": f"Hi! I'm {self.name}, here to help with geometry!",
            "help": f"I'm {self.name}, specializing in {self.specialization}. I can help with: cubes, spheres, cones, cylinders, triangles, rectangles.",
            "formula": "I can provide formulas for volume, surface area, and area of geometric shapes.",
            "shapes": "I know about: Cube, Sphere, Cone, Cylinder, Triangle, Rectangle.",
            "progress": "I can help you track your learning progress and suggest areas to improve.",
            "quiz": "Ready for a quiz? I can test your knowledge of geometric shapes and formulas.",
            "practice": "Let's practice some geometry problems together!"
        }
    
    def get_response(self, message, user_id):
        msg_lower = message.lower()
        
        # Check matches 
        for key in self.responses:
            if key == msg_lower:
                return self.responses[key]
        
        # Check for partial matches
        for key in self.responses:
            if key in msg_lower:
                return self.responses[key]
        
        # Default response
        return f"I'm {self.name}, your geometry tutor. I can help with shapes, formulas, quizzes, and practice exercises. What would you like to know?"

# Initialize managers
progress_manager = ProgressManager()
ai_tutor = AITutor()

# Ensure required directories exist
def ensure_directories():
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    frontend_dir = Path("../frontend")
    frontend_dir.mkdir(exist_ok=True)
    
    images_dir = Path("../frontend/images")
    images_dir.mkdir(exist_ok=True)
    
    # Create default files if they don't exist
    users_file = data_dir / "users.json"
    if not users_file.exists():
        with open(users_file, 'w') as f:
            json.dump({"students": [], "guests": []}, f)
    
    progress_file = data_dir / "progress.json"
    if not progress_file.exists():
        with open(progress_file, 'w') as f:
            json.dump({}, f)

# ==================== API ROUTES ====================

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend', path)

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login with ontology support"""
    data = request.json
    username = data.get('username', '').strip()
    is_guest = data.get('guest', False)
    
    if is_guest:
        user = auth_manager.create_guest_user()
        user["from_ontology"] = False
    else:
        if not username:
            return jsonify({"error": "Username required"}), 400
        
        #  check if user exists in ontology
        ontology_user = None
        if ontology_loader and hasattr(ontology_loader, 'get_all_students'):
            students = ontology_loader.get_all_students()
            for student in students:
                student_name = student.get('name', '').lower()
                if username.lower() in student_name:
                    ontology_user = student
                    break
        
        if ontology_user:
            # if User found in ontology
            user = {
                "user_id": ontology_user.get('name', f"student_{username}").replace(' ', '_').lower(),
                "name": ontology_user.get('name', username),
                "type": "student",
                "from_ontology": True,
                "details": ontology_user.get('details', {}),
                "properties": ontology_user.get('properties', {})
            }
            print(f"User {username} authenticated from ontology")
        else:
            # if User not in ontology, use default auth
            user = auth_manager.login_user(username)
            user["from_ontology"] = False
    
    return jsonify(user)

@app.route('/api/shapes', methods=['GET'])
def get_shapes():
    """Get geometric shapes with ontology enhancement"""
    print("\n🔍 Getting shapes with ontology data...")
    
    # Base hardcoded shapes
    base_shapes = [
        {"name": "Cube", "formula": "Volume = a³", "image": "cube1.jpg", "type": "Cube", "category": "3D"},
        {"name": "Sphere", "formula": "Volume = 4/3 π r³", "image": "sphere1.png", "type": "Sphere", "category": "3D"},
        {"name": "Cone", "formula": "Volume = (1/3) π r² h", "image": "cone1.png", "type": "Cone", "category": "3D"},
        {"name": "Cylinder", "formula": "Volume = π r² h", "image": "cylinder.jpg", "type": "Cylinder", "category": "3D"},
        {"name": "Triangle", "formula": "Area = 1/2 × base × height", "image": "triangle.png", "type": "Triangle", "category": "2D"},
        {"name": "Rectangle", "formula": "Area = length × width", "image": "rectangle.jpg", "type": "Rectangle", "category": "2D"}
    ]
    
    enhanced_shapes = []
    ontology_used = False
    
    if ontology_loader:
        try:
            # Get shapes from ontology
            if hasattr(ontology_loader, 'get_all_shapes_with_formulas'):
                ontology_shapes = ontology_loader.get_all_shapes_with_formulas()
                
                if ontology_shapes:
                    ontology_used = True
                    print(f"Found {len(ontology_shapes)} shapes in ontology")
                    
                    # Use ontology shapes
                    for shape in ontology_shapes:
                        enhanced_shape = {
                            "name": shape.get('name', 'Unknown'),
                            "type": shape.get('type', 'Shape'),
                            "category": shape.get('category', '3D'),
                            "uri": shape.get('uri', ''),
                            "from_ontology": True,
                            "formulas": shape.get('formulas', []),
                            "properties": shape.get('properties', {})
                        }
                        
                        # Add formula 
                        if shape.get('formulas'):
                            enhanced_shape["formula"] = shape['formulas'][0].get('expression', 'See formulas')
                        else:
                            # Fallback to base formula
                            base_match = next((b for b in base_shapes if b['name'].lower() == shape['name'].lower()), None)
                            enhanced_shape["formula"] = base_match['formula'] if base_match else "Formula available"
                        
                        # Add image
                        base_match = next((b for b in base_shapes if b['name'].lower() == shape['name'].lower()), None)
                        enhanced_shape["image"] = base_match['image'] if base_match else ""
                        
                        enhanced_shapes.append(enhanced_shape)
            
            # If no ontology shapes, use base shapes with ontology info
            if not enhanced_shapes:
                for shape in base_shapes:
                    enhanced_shape = shape.copy()
                    enhanced_shape["source"] = "hardcoded"
                    
                    # Check shape class exists in ontology
                    if shape["type"] in ontology_loader.classes:
                        enhanced_shape["uri"] = ontology_loader.classes[shape["type"]].get('uri', '')
                        enhanced_shape["from_ontology"] = True
                        ontology_used = True
                    
                    enhanced_shapes.append(enhanced_shape)
                    
        except Exception as e:
            print(f" Error getting shapes from ontology: {e}")
            enhanced_shapes = base_shapes
            for shape in enhanced_shapes:
                shape["source"] = "hardcoded"
                shape["from_ontology"] = False
    else:
        enhanced_shapes = base_shapes
        for shape in enhanced_shapes:
            shape["source"] = "hardcoded"
            shape["from_ontology"] = False
    
    return jsonify({
        "shapes": enhanced_shapes,
        "count": len(enhanced_shapes),
        "ontology_used": ontology_used,
        "ai_tutor": ai_tutor.name,
        "ai_tutor_from_ontology": ai_tutor.from_ontology
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from ontology and system"""
    try:
        # Get users from ontology
        ontology_students = []
        if ontology_loader and hasattr(ontology_loader, 'get_all_students'):
            ontology_students = ontology_loader.get_all_students()
            print(f"✅ Found {len(ontology_students)} students in ontology")
        
        # get users from JSON file
        try:
            users_file = Path("../data/users.json")
            if users_file.exists():
                with open(users_file, 'r') as f:
                    json_users = json.load(f)
            else:
                json_users = {"students": [], "guests": []}
        except Exception as e:
            print(f"Error loading JSON users: {e}")
            json_users = {"students": [], "guests": []}
        
        # Prepare ontology students for response
        ontology_students_formatted = []
        for student in ontology_students:
            ontology_students_formatted.append({
                "username": student.get('name', 'Unknown').split(' - ')[0].replace(' ', '_').lower(),
                "name": student.get('name', 'Unknown'),
                "type": "student",
                "from_ontology": True,
                "details": student.get('details', {}),
                "properties": student.get('properties', {})
            })
        
        # Prepare response
        response = {
            "from_ontology": ontology_students_formatted,
            "from_json": json_users,
            "ontology_user_count": len(ontology_students_formatted),
            "json_student_count": len(json_users.get("students", [])),
            "json_guest_count": len(json_users.get("guests", [])),
            "total_users": len(ontology_students_formatted) + len(json_users.get("students", [])) + len(json_users.get("guests", [])),
            "ai_tutor": ai_tutor.name,
            "ai_tutor_from_ontology": ai_tutor.from_ontology
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in get_users: {e}")
        return jsonify({
            "error": str(e),
            "users": [],
            "total_users": 0
        })

# ============== ONTOLOGY POWERED ENDPOINTS ==============

@app.route('/api/ontology/classes', methods=['GET'])
def get_ontology_classes():
    """Get all classes from ontology"""
    if not ontology_loader:
        return jsonify({"error": "Ontology not loaded"})
    
    classes_by_category = {}
    if hasattr(ontology_loader, 'get_classes_by_category'):
        classes_by_category = {
            'user': ontology_loader.get_classes_by_category('user'),
            'authentication': ontology_loader.get_classes_by_category('authentication'),
            'learning': ontology_loader.get_classes_by_category('learning'),
            'geometry': ontology_loader.get_classes_by_category('geometry'),
            'progress': ontology_loader.get_classes_by_category('progress')
        }
    
    return jsonify({
        'status': 'success',
        'classes_by_category': classes_by_category,
        'total_classes': len(ontology_loader.classes) if hasattr(ontology_loader, 'classes') else 0
    })

@app.route('/api/ontology/students', methods=['GET'])
def get_ontology_students():
    """Get all students from ontology"""
    if not ontology_loader:
        return jsonify({"error": "Ontology not loaded"}), 400
    
    try:
        students = ontology_loader.get_all_students() if hasattr(ontology_loader, 'get_all_students') else []
        return jsonify({
            'status': 'success',
            'students': students,
            'total_students': len(students)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============THE MAIN EXECUTION ==============

if __name__ == '__main__':
    # Ensure directories exist
    ensure_directories()
    
    # Print available routes
    print("\n Available Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule}")
    
    # Run the app
    print(f"\n Starting Flask server on http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)