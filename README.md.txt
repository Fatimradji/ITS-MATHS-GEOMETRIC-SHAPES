# Geometry Intelligent Tutoring System - Ontology

##  Overview
This ontology models an **Intelligent Tutoring System (ITS)** for geometry education, designed to support personalized learning experiences through structured knowledge representation of geometric concepts, student interactions, and adaptive tutoring strategies.

##   Purpose
- **Domain**: Learning of Geometry shapes & Intelligent Tutoring Systems
- **Objective**: Create a semantic framework for adaptive geometry learning
- **Application**: Support AI-driven tutoring with personalized interventions

## Ontology Design
View images(MY ONTOLOGY.png)


### Core Components
Object-property1/png
Object-property2.png
Individual-properties.png
Entitiies-class-ussage.png
myclass-hieararchy.png


#### 1. **User Management System**
User
├── Student (Registered learners)
├── Tutor (Teaching entities)
│ └── AITutor (Artificial intelligence tutors)
└── GuestUser (Temporary access users)

#### 2. **Geometric Knowledge Base**

GeometricShape
├── TwoDShape (2-dimensional shapes)
│ ├── Triangle
│ ├── Rectangle
│ └── [Other 2D shapes]
└── ThreeDShape (3-dimensional shapes)
├── Cube
├── Sphere
├── Cylinder
├── Cone
└── [Other 3D shapes]

#### 3. **Learning Framework**
- **LearningActivity**: Educational exercises and tasks
- **LearningDifficulty**: Identified student challenges
- **Intervention**: Teaching strategies and support mechanisms
- **Progress**: Student performance tracking.


#### 4. **Session Management**
LoginSession
├── RegisteredSession (Logged-in users)
└── GuestSession (Temporary sessions)



### Key Relationships & Properties

| Relationship | Description | Domain → Range |
|--------------|-------------|----------------|
| `hasTutor`   | Student-tutor assignment | Student → Tutor |
| `addresses
  Difficulty`  | Problem resolution | Intervention → LearningDifficulty |
| `conductedBy`| Session leadership | TutoringSession → Tutor |
| `hasActiveSession` | User session tracking | User → LoginSession |
| `measuresProgress` | Performance assessment | LearningActivity → Progress |

## File Structure

geometry-its-ontology/
├── README.md # This file
│── my ITS geometry shapes for maths.owl # My Main OWL ontology
│── my intelligent tutoring system maths geo shapes.html # HTML documentation Including Css , PYthon
├── screenshots/ # Visual representations
│── MY ONTOLOGY.png
│── DATA-PROPERTIES.png
│── OBJECT-PROPERTIES.png


## Technical Specifications

### Ontology Metrics
- **Classes**: 20+ structured entities
- **Object Properties**: 15+ relationships
- **Data Properties**: 10+ attributes
- **Individuals**: Concrete instances and examples
- **Axioms**: Logical constraints and rules

### Namespace

Base URI: http://www.semanticweb.org/ontology/its-geometry#


## Usage Instructions

### 1. Viewing the Ontology
- **Primary Tool**: Protégé Desktop Editor
- **Online Visualization**: WebVOWL or similar tools
- **Documentation**: Open `documentation/my intelligent tutoring system maths geo shapes.html` in browser

### 2. Loading in Protégé
1. Open Protégé
2. File → Open → Select `my ITS geometry shapes for maths.owl`
3. Explore different tabs:
   - **Entities**: Class hierarchy and properties
   - **OWL Viz**: Visual representation
   - **DL Query**: Advanced reasoning

### 3. Integration Possibilities
- AI tutoring system backend
- Student progress analytics
- Adaptive learning path generation
- Geometry knowledge representation

## Key Design Decisions

### 1. Modular Architecture
Separated concerns into:
- **User Management** (authentication, sessions)
- **Domain Knowledge** (geometry concepts)
- **Learning Process** (activities, progress, interventions)

### 2. Extensibility
- Easy to add new geometric shapes
- Scalable user types and roles
- Flexible intervention strategies

### 3. Practical Implementation
- Real-world tutoring scenarios
- Concrete student and tutor examples
- Measurable progress tracking

## Visual Documentation

The ontology includes comprehensive visual documentation:
- **Class Hierarchy**: Inheritance relationships
- **Property Usage**: Relationship implementations
- **Instance Examples**: Concrete usage scenarios

## Future Enhancements that I wll be adding in the futur

- [ ] more geometric shapes and formulas
- [ ] Implementing reasoning rules for adaptive learning
- [ ] Integrate it with tutoring system frontend
- [ ] Extend with learning analytics capabilities

## Academic Context

This work demonstrates:
- **Ontology Engineering** principles
- **Domain Modeling** for education technology
- **Semantic Web** technologies application
- **Intelligent Systems** design patterns

## License

This ontology is available for academic and research purposes. Please cite appropriately if used in research projects.

## Contributing

For suggestions or improvements:
1. For the repository
2. Create a feature branch
3. Submit a pull request with detailed explanation

## Contact Me

For questions about this ontology:
- **Student**: RADJI FATIM
- **Institution**: York st john University
- **Course**: MSC COMPUTER SCIENCE
- **Supervisor**: Dr. Sahar Ahmadzadeh

*Last updated: 30.11.2025*












