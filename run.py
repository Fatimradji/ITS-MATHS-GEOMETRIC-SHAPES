import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Add to Python path
sys.path.insert(0, current_dir)

# Check if required files exist
print("\nChecking files...")
files_to_check = [
    ("backend/app.py", os.path.join(current_dir, "backend", "app.py")),
    ("ontology/my_ontologyIts.xml", os.path.join(current_dir, "ontology", "my_ontologyIts.xml")),
    ("ontology/ontology_loader.py", os.path.join(current_dir, "ontology", "ontology_loader.py"))
]

for name, path in files_to_check:
    if os.path.exists(path):
        print(f"✓ {name} found")
    else:
        print(f"✗ {name} NOT FOUND at: {path}")

print("\n" + "="*60)
print("Starting Intelligent Tutoring System...")
print("="*60)

try:
    from backend.app import app
    print("✓ Flask app imported successfully")
    
    if __name__ == '__main__':
        print(f"\nServer starting on: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        app.run(debug=True, port=5000, use_reloader=False)
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Install required packages: pip install flask flask-cors owlready2")
    print("2. Make sure all files are in correct locations")
    print("3. Check if port 5000 is already in use")
    input("\nPress Enter to exit...")