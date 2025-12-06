import os
import xml.etree.ElementTree as ET
import json
from collections import defaultdict  # Added import

class OntologyLoader:
    def __init__(self, ontology_path="ontology/my_ontologyIts.xml"):
        # Convert to absolute path
        if not os.path.isabs(ontology_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            ontology_path = os.path.join(project_root, ontology_path)
        
        self.ontology_path = ontology_path
        self.classes = {}
        self.individuals = []
        self.class_hierarchy = defaultdict(list)  # Using defaultdict here
        self.loaded = False
        print(f"OntologyLoader initialized with path: {self.ontology_path}")
        
    def load_ontology(self):
        """Load and parse the OWL ontology"""
        try:
            # Check if file exists
            if not os.path.exists(self.ontology_path):
                print(f"Error: Ontology file not found at {self.ontology_path}")
                self._create_sample_data()
                return False
            
            # Parse the XML file
            tree = ET.parse(self.ontology_path)
            root = tree.getroot()
            
            # Define namespace
            ns = {
                'owl': 'http://www.w3.org/2002/07/owl#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#'
            }
            
            # Extract classes with hierarchy
            for class_elem in root.findall('.//owl:Class', ns):
                class_uri = class_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
                if class_uri:
                    class_name = class_uri.split('#')[-1]
                    
                    # Get label
                    label_elem = class_elem.find('.//rdfs:label', ns)
                    label = label_elem.text if label_elem is not None else class_name
                    
                    # Get comment/description
                    comment_elem = class_elem.find('.//rdfs:comment', ns)
                    comment = comment_elem.text if comment_elem is not None else ''
                    
                    # Get subclass relationships
                    subclass_elem = class_elem.find('.//rdfs:subClassOf', ns)
                    parent_class = ''
                    if subclass_elem is not None:
                        parent_resource = subclass_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                        if parent_resource:
                            parent_class = parent_resource.split('#')[-1]
                    
                    self.classes[class_name] = {
                        'uri': class_uri,
                        'label': label,
                        'comment': comment,
                        'parent': parent_class,
                        'type': 'class'
                    }
                    
                    # Build hierarchy
                    if parent_class:
                        self.class_hierarchy[parent_class].append(class_name)
            
            # Extract individuals
            for indiv_elem in root.findall('.//*[@rdf:about]', ns):
                indiv_uri = indiv_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
                
                # Get the type
                type_elem = indiv_elem.find('.//rdf:type', ns)
                if type_elem is not None:
                    type_resource = type_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                    if type_resource:
                        type_name = type_resource.split('#')[-1]
                        
                        individual = {
                            'uri': indiv_uri,
                            'type': type_name,
                            'properties': {}
                        }
                        
                        # Get label
                        label_elem = indiv_elem.find('.//rdfs:label', ns)
                        if label_elem is not None:
                            individual['label'] = label_elem.text
                        else:
                            individual['label'] = type_name
                        
                        # Get comment
                        comment_elem = indiv_elem.find('.//rdfs:comment', ns)
                        if comment_elem is not None:
                            individual['comment'] = comment_elem.text
                        
                        # Get all properties
                        for prop_elem in indiv_elem:
                            tag = prop_elem.tag
                            if '}' in tag:
                                prop_name = tag.split('}')[1]
                                if prop_name not in ['type', 'label', 'comment']:
                                    # Get property value
                                    if prop_elem.text:
                                        individual['properties'][prop_name] = prop_elem.text
                                    elif '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in prop_elem.attrib:
                                        resource = prop_elem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                                        individual['properties'][prop_name] = resource.split('#')[-1]
                                    elif '{http://www.w3.org/2001/XMLSchema#}datatype' in prop_elem.attrib:
                                        # Handle datatype properties
                                        datatype = prop_elem.attrib['{http://www.w3.org/2001/XMLSchema#}datatype']
                                        individual['properties'][prop_name] = {
                                            'value': prop_elem.text,
                                            'datatype': datatype
                                        }
                        
                        self.individuals.append(individual)
            
            self.loaded = True
            
            # Print comprehensive summary
            self._print_ontology_summary()
            
            return True
            
        except Exception as e:
            print(f" Error loading ontology: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _print_ontology_summary(self):
        """Print detailed ontology summary"""
        print("\n" + "="*60)
        print("  ONTOLOGY LOADED SUCCESSFULLY")
        print("="*60)
        
        print(f"\n  STATISTICS:")
        print(f"   Total Classes: {len(self.classes)}")
        print(f"   Total Individuals: {len(self.individuals)}")
        
        print(f"\n  CLASS HIERARCHY:")
        for parent, children in self.class_hierarchy.items():
            print(f"   {parent}: {', '.join(children)}")
        
        print(f"\n USER-RELATED CLASSES:")
        user_classes = [c for c in self.classes.keys() if 'user' in c.lower() or 'student' in c.lower() or 'tutor' in c.lower()]
        for cls in user_classes:
            info = self.classes[cls]
            print(f"   • {cls}: {info.get('label', '')} - {info.get('comment', '')[:50]}...")
        
        print(f"\n📐 GEOMETRY-RELATED CLASSES:")
        geometry_classes = [c for c in self.classes.keys() if 'shape' in c.lower() or 'cube' in c or 'sphere' in c or 'formula' in c.lower()]
        for cls in geometry_classes:
            info = self.classes[cls]
            print(f"   • {cls}: {info.get('label', '')}")
        
        print(f"\n INDIVIDUALS BY CATEGORY:")
        categories = defaultdict(list)  # Using defaultdict here
        for ind in self.individuals:
            categories[ind['type']].append(ind['label'])
        
        for category, items in categories.items():
            print(f"   {category} ({len(items)}): {', '.join(items[:3])}{'...' if len(items) > 3 else ''}")
        
        print("="*60)
    
    def get_classes_by_category(self, category):
        """Get classes by category"""
        if not self.loaded:
            return []
        
        categories = {
            'user': ['User', 'Student', 'GuestUser', 'Tutor', 'AITutor', 'HumanTutor'],
            'authentication': ['Authentication', 'LoginSession', 'UserAccount', 'GuestSession', 'RegisteredSession'],
            'learning': ['LearningDifficulty', 'TutoringSession', 'Intervention', 'LearningActivity'],
            'geometry': ['GeometricShape', 'ThreeDShape', 'TwoDShape', 'Cube', 'Sphere', 'Cone', 'Cylinder', 'Triangle', 'Rectangle', 'Formula'],
            'progress': ['Progress']
        }
        
        if category in categories:
            return [self.classes[cls] for cls in categories[category] if cls in self.classes]
        return []
    
    def get_all_students(self):
        """Get all Student individuals with detailed info"""
        if not self.loaded:
            return []
        
        students = []
        for individual in self.individuals:
            if individual.get('type') == 'Student':
                student_data = {
                    'name': individual.get('label', 'Unknown Student'),
                    'type': 'Student',
                    'uri': individual.get('uri', ''),
                    'properties': individual.get('properties', {}),
                    'details': {}
                }
                
                # Extract specific properties
                props = individual.get('properties', {})
                if 'studentName' in props:
                    student_data['details']['full_name'] = props['studentName']
                if 'hasAccount' in props:
                    student_data['details']['account'] = props['hasAccount']
                if 'hasActiveSession' in props:
                    student_data['details']['active_session'] = props['hasActiveSession']
                if 'hasTutor' in props:
                    student_data['details']['tutor'] = props['hasTutor']
                
                students.append(student_data)
        
        return students
    
    def get_all_shapes_with_formulas(self):
        """Get all geometric shapes with their formulas"""
        if not self.loaded:
            return []
        
        shapes = []
        
        # First, get all shape individuals
        for individual in self.individuals:
            indiv_type = individual.get('type', '')
            if indiv_type in ['Cube', 'Sphere', 'Cone', 'Cylinder', 'Triangle', 'Rectangle']:
                shape_data = {
                    'name': individual.get('label', indiv_type),
                    'type': indiv_type,
                    'category': '3D' if indiv_type in ['Cube', 'Sphere', 'Cone', 'Cylinder'] else '2D',
                    'uri': individual.get('uri', ''),
                    'properties': individual.get('properties', {}),
                    'formulas': []
                }
                
                # Look for associated formulas
                props = individual.get('properties', {})
                formula_props = [k for k in props.keys() if 'formula' in k.lower()]
                for prop in formula_props:
                    formula_uri = props[prop]
                    # Find the formula individual
                    for formula_ind in self.individuals:
                        if formula_ind.get('uri', '').endswith(f'#{formula_uri}') or formula_uri in formula_ind.get('uri', ''):
                            formula_expr = formula_ind.get('properties', {}).get('formulaExpression', '')
                            if formula_expr:
                                shape_data['formulas'].append({
                                    'type': prop.replace('has', '').replace('Formula', '').strip(),
                                    'expression': formula_expr,
                                    'source': 'ontology'
                                })
                
                shapes.append(shape_data)
        
        # If no shape individuals, create from classes
        if not shapes:
            shape_classes = ['Cube', 'Sphere', 'Cone', 'Cylinder', 'Triangle', 'Rectangle']
            for cls_name in shape_classes:
                if cls_name in self.classes:
                    shapes.append({
                        'name': self.classes[cls_name].get('label', cls_name),
                        'type': cls_name,
                        'category': '3D' if cls_name in ['Cube', 'Sphere', 'Cone', 'Cylinder'] else '2D',
                        'uri': self.classes[cls_name].get('uri', ''),
                        'formulas': [],
                        'from_class': True
                    })
        
        return shapes
    
    def get_learning_activities(self):
        """Get learning activities from ontology"""
        if not self.loaded:
            return []
        
        activities = []
        for individual in self.individuals:
            if individual.get('type') == 'LearningActivity':
                activities.append({
                    'name': individual.get('label', 'Learning Activity'),
                    'type': 'LearningActivity',
                    'uri': individual.get('uri', ''),
                    'properties': individual.get('properties', {})
                })
        
        return activities
    
    def get_progress_data(self):
        """Get progress tracking data"""
        if not self.loaded:
            return []
        
        progress_data = []
        for individual in self.individuals:
            if individual.get('type') == 'Progress':
                progress = {
                    'name': individual.get('label', 'Progress'),
                    'type': 'Progress',
                    'uri': individual.get('uri', ''),
                    'metrics': {}
                }
                
                # Extract progress metrics
                props = individual.get('properties', {})
                if 'quizScore' in props:
                    progress['metrics']['quiz_score'] = props['quizScore']
                if 'practiceScore' in props:
                    progress['metrics']['practice_score'] = props['practiceScore']
                if 'completionPercentage' in props:
                    progress['metrics']['completion_percentage'] = props['completionPercentage']
                if 'lastActivityDate' in props:
                    progress['metrics']['last_activity'] = props['lastActivityDate']
                
                progress_data.append(progress)
        
        return progress_data
    
    def get_tutoring_sessions(self):
        """Get tutoring sessions data"""
        if not self.loaded:
            return []
        
        sessions = []
        for individual in self.individuals:
            if individual.get('type') == 'TutoringSession':
                session = {
                    'name': individual.get('label', 'Tutoring Session'),
                    'type': 'TutoringSession',
                    'uri': individual.get('uri', ''),
                    'properties': individual.get('properties', {})
                }
                sessions.append(session)
        
        return sessions
    
    def get_ai_tutor(self):
        """Get AI Tutor with enhanced search"""
        if not self.loaded:
            return None
        
        print("\n Searching for AI Tutor...")
        
        # Multiple search strategies
        search_patterns = [
            ('type', 'AITutor'),
            ('type', 'Tutor'),
            ('label', 'FATIM'),
            ('label', 'Tutor'),
            ('uri', 'TutorFATIM')
        ]
        
        for individual in self.individuals:
            for field, pattern in search_patterns:
                value = individual.get(field, '').lower()
                if pattern.lower() in value:
                    print(f"Found AI Tutor by {field}: {individual.get('label')}")
                    
                    tutor_data = {
                        'name': individual.get('label', 'AI Tutor'),
                        'type': individual.get('type', 'AITutor'),
                        'uri': individual.get('uri', ''),
                        'properties': individual.get('properties', {}),
                        'specialization': individual.get('properties', {}).get('tutorSpecialization', 'Geometry'),
                        'from_ontology': True
                    }
                    
                    print(f"   Name: {tutor_data['name']}")
                    print(f"   Specialization: {tutor_data['specialization']}")
                    
                    return tutor_data
        
        print("AI Tutor not found in individuals, checking if we should create from known structure")
        
        # If not found but we know it should exist
        return {
            'name': 'FATIM AI Tutor',
            'type': 'AITutor',
            'specialization': 'Geometric Shapes and Formulas',
            'from_ontology': True,
            'inferred': True
        }
    
    def get_ontology_stats(self):
        """Get comprehensive ontology statistics"""
        if not self.loaded:
            return {}
        
        return {
            'total_classes': len(self.classes),
            'total_individuals': len(self.individuals),
            'user_classes': len([c for c in self.classes.keys() if 'user' in c.lower() or 'student' in c.lower() or 'tutor' in c.lower()]),
            'geometry_classes': len([c for c in self.classes.keys() if 'shape' in c.lower() or 'formula' in c.lower()]),
            'learning_classes': len([c for c in self.classes.keys() if 'learning' in c.lower() or 'session' in c.lower() or 'progress' in c.lower()]),
            'students': len([i for i in self.individuals if i.get('type') == 'Student']),
            'tutors': len([i for i in self.individuals if 'tutor' in i.get('type', '').lower()]),
            'shapes': len([i for i in self.individuals if i.get('type') in ['Cube', 'Sphere', 'Cone', 'Cylinder', 'Triangle', 'Rectangle']]),
            'sessions': len([i for i in self.individuals if 'session' in i.get('type', '').lower()]),
            'progress_records': len([i for i in self.individuals if i.get('type') == 'Progress'])
        }
    
    def _create_sample_data(self):
        """Create sample data if ontology loading fails"""
        print("⚠️ Creating sample ontology data...")
        self.classes = {
            'Student': {'uri': '#Student', 'label': 'Student', 'type': 'class'},
            'GuestUser': {'uri': '#GuestUser', 'label': 'Guest User', 'type': 'class'},
            'Tutor': {'uri': '#Tutor', 'label': 'Tutor', 'type': 'class'},
            'AITutor': {'uri': '#AITutor', 'label': 'AI Tutor', 'type': 'class'},
            'Cube': {'uri': '#Cube', 'label': 'Cube', 'type': 'class'},
            'Sphere': {'uri': '#Sphere', 'label': 'Sphere', 'type': 'class'},
            'Cone': {'uri': '#Cone', 'label': 'Cone', 'type': 'class'},
            'Cylinder': {'uri': '#Cylinder', 'label': 'Cylinder', 'type': 'class'},
            'Triangle': {'uri': '#Triangle', 'label': 'Triangle', 'type': 'class'},
            'Rectangle': {'uri': '#Rectangle', 'label': 'Rectangle', 'type': 'class'}
        }
        
        self.individuals = [
            {
                'uri': '#StudentJohn',
                'type': 'Student',
                'label': 'John - Registered Student',
                'properties': {'studentName': 'John', 'hasAccount': 'JohnAccount'}
            },
            {
                'uri': '#StudentSarah',
                'type': 'Student',
                'label': 'Sarah - Registered Student',
                'properties': {'studentName': 'Sarah', 'hasAccount': 'SarahAccount'}
            }
        ]
        
        self.loaded = True
        print("Sample ontology data created successfully")