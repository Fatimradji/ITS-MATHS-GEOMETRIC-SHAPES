I- Project Overview

An Intelligent Tutoring System for teaching Geometry concepts, built with semantic web technologies and modern web development.

Domain: Geometry Education
System: AI-powered tutoring system for geometric shapes and formulas
Status: Working Prototype
Demo: http://localhost:5000 (when running locally)

 II-Core Features
 
AI-Powered Tutoring: FAITH AI Tutor with geometry specialization

Ontology-Driven Content: Geometric shapes and formulas from OWL ontology

Interactive Learning: Quiz, practice exercises, and progress tracking

User Management: Guest and student login with progress persistence

Responsive Design: Modern web interface accessible on all devices

 III-Ontology Integration
 Shapes data loaded from Protégé OWL file

 AI Tutor information extracted from ontology

 Student profiles linked to ontology individuals

 Dynamic content generation based on semantic relationships

     IV-Technical Features
     
RESTful API with Flask backend

Real-time progress tracking

JSON data persistence

CORS-enabled for frontend-backend communication

Modular architecture for easy extension

V- Architecture

Frontend (Browser)
    ↓ HTTP Requests
Backend API (Flask/Python)
    ↓ Ontology Queries
Semantic Layer (OWL/RDF)
    ↓ Data Storage
JSON Files + OWL Ontology

VI-Project Structure

ITS FOLDER PY/
├── backend/                    # Flask application
│   ├── app.py                 # Main Flask server
│   ├── auth.py               # Authentication module
│   ├── ontology_loader.py    # OWL file parser
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # Web interface
│   ├── index.html            # Main application
│   ├── style.css             # Styling
│   ├── script.js             # Frontend logic
│   └── images/               # Shape images
│
├── ontology/                  # Semantic layer
│   └── my_ontologyIts.xml    # Protégé OWL file
│
├── data/                     # JSON data storage
│   ├── users.json            # User accounts
│   └── progress.json         # Learning progress
│
└── README.md                 # This file

VII-Prerequisites

Python 3.8+
pip (Python package manager)
Modern web browser

-Installation

(Bash  you will have to name the main folder ITS FOLDER PY  after dowloading the remainnig file from my GITHUB or give it your chouce name )
# Navigate to project directory
cd "C:\xampp\htdocs\ITS FOLDER PY"

-Install Python dependencies

cd backend
pip install -r requirements.txt

-Start the Flask server

python app.py

 -Access the application
 
 Open your browser
Navigate to: http://localhost:5000

- Using the System
- 
  As a Guest User
Visit http://localhost:5000
Click "Continue as Guest"
Explore shapes, take quizzes, practice exercises

-As a Registered Student

Visit http://localhost:5000
Enter your name
Click "Start Learning"
Track progress across sessions

-Available Sections
Home: Welcome and login
Shapes: View geometric shapes with formulas
Quiz: Test your knowledge
Practice: Interactive exercises
Progress: Track learning achievements
Dashboard: Personal learning analytics

-API Endpoints

Endpoint	Method	Description	Example Response
/api/shapes	GET	Get all geometric shapes	{shapes: [...], ontology_used: true}
/api/login	POST	Authenticate user	{user_id: "guest_001", name: "Guest"}
/api/users	GET	Get all users	{from_ontology: [...], from_json: [...]}
/api/ontology/classes	GET	Get ontology classes	{classes_by_category: {...}}
/api/ontology/students	GET	Get students from ontology	{students: [...], total_students: 5}

-Example API Usage

# Get shapes data
curl http://localhost:5000/api/shapes

# Test API with Python
python -c "import requests; print(requests.get('http://localhost:5000/api/shapes').json())"

-Ontology Design

Classes (Protégé)
text
GeometricShape
├── ThreeDShape (Cube, Sphere, Cone, Cylinder)
└── TwoDShape (Triangle, Rectangle)

User
├── Student
└── Guest

AI_Tutor
Progress
Formula
LearningActivity

-Key Individuals
FAITH_AI_Tutor: Main tutoring agent

Cube, Sphere, Cone, Cylinder, Triangle, Rectangle: Geometric shapes

John_Doe, Jane_Smith: Example students

-Properties

hasFormula: Links shapes to their formulas
hasVolume: 3D shape volume formulas
hasSurfaceArea: Surface area calculations
teaches: AI Tutor to Student relationship
tracksProgress: Progress monitoring

-Development

Extending the Ontology
Open ontology/my_ontologyIts.xml in Protégé
Add new classes, properties, or individuals
Export as RDF/XML
Restart Flask server

System Requirements

Software Requirements
Backend: Python 3.8+, Flask, rdflib
Frontend: Modern browser (Chrome 90+, Firefox 88+, Safari 14+)
Ontology Editor: Protégé (for development)

-Hardware Requirements
Minimum: 2GB RAM, 1GHz processor
Recommended: 4GB RAM, 2GHz processor
Storage: 100MB free space

-Future Enhancements

Planned Features
3D shape visualizations with WebGL
Voice interaction with AI Tutor
Mobile app (React Native)
Advanced adaptive learning algorithms
Gamification elements (badges, leaderboards)
Multi-language support
Teacher dashboard for classroom management

-Development Team
Ontology Design:RADJI FATIM

Backend Development: RADJI FATIM

Frontend Development: RADJI FATIM
System Integration: RADJI FATIM

-Academic Context

This project was developed as part of an Intelligent Systems course, demonstrating:
Semantic web technologies (OWL, RDF)
Intelligent Tutoring System design
Full-stack web development
Ontology-driven application architecture

- License
This project is for educational purposes. All rights reserved.

Usage Rights
 Educational use
 Research purposes
 Academic projects
 Commercial use without permission
 Redistribution without attribution  

 - Support & Contact
For questions or support:

Email: Fatimradji12@gmail.com

Course: MSC.COMPUTER SCIENCE/COM7032M 

Institution: YORK ST JOHN UNIVERSITY LONDON

-Last Updated: December 12/6/2025
Version: 1.0.0
Status: Production Ready

"geometry education through intelligent tutoring system "

