import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Testing imports from:", current_dir)
print("-" * 50)

# Test imports
modules_to_test = [
    ("backend.auth", "auth.py"),
    ("backend.progress", "progress.py"), 
    ("backend.tutor", "tutor.py"),
    ("backend.app", "app.py"),
    ("ontology.ontology_loader", "ontology/ontology_loader.py")
]

for module_name, file_path in modules_to_test:
    try:
        __import__(module_name)
        print(f"✓ {module_name} imported successfully")
    except ImportError as e:
        print(f"✗ {module_name} failed: {e}")
    except Exception as e:
        print(f"✗ {module_name} error: {type(e).__name__}: {e}")

print("-" * 50)
input("Press Enter to continue...")