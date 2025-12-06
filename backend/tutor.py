import random

class AITutor:
    def __init__(self):
        self.knowledge_base = {
            "cube": {
                "volume": "Volume of a cube = a³ (where 'a' is the side length). Example: If side = 4 cm, volume = 4³ = 64 cm³",
                "surface_area": "Surface area of a cube = 6a². This is because a cube has 6 faces, each with area a²",
                "description": "A cube is a 3D shape with 6 square faces, 12 edges, and 8 vertices. All edges are equal in length."
            },
            "sphere": {
                "volume": "Volume of a sphere = 4/3 π r³ (where 'r' is the radius). π is approximately 3.14159",
                "surface_area": "Surface area of a sphere = 4πr². This formula gives the total area covering the sphere",
                "description": "A sphere is a perfectly round 3D shape like a ball. All points on the surface are equidistant from the center."
            },
            "cone": {
                "volume": "Volume of a cone = (1/3) π r² h (where 'r' is radius, 'h' is height)",
                "surface_area": "Surface area of a cone = πr(r + l) where 'l' is the slant height",
                "description": "A cone has a circular base and tapers smoothly to a point called the apex."
            },
            "cylinder": {
                "volume": "Volume of a cylinder = π r² h (area of circular base × height)",
                "surface_area": "Surface area = 2πr(h + r) = area of side + area of both circular ends",
                "description": "A cylinder has two parallel circular bases connected by a curved surface."
            },
            "triangle": {
                "area": "Area of a triangle = 1/2 × base × height",
                "perimeter": "Perimeter = sum of all three sides",
                "description": "A triangle is a 3-sided polygon. The sum of interior angles is always 180°."
            },
            "rectangle": {
                "area": "Area of a rectangle = length × width",
                "perimeter": "Perimeter = 2 × (length + width)",
                "description": "A rectangle has 4 sides with opposite sides equal and all angles 90°."
            },
            "general": {
                "2d_vs_3d": "2D shapes are flat with only length and width (like triangle, rectangle). 3D shapes have length, width, and height (like cube, sphere).",
                "pi": "π (pi) is a mathematical constant approximately equal to 3.14159. It represents the ratio of a circle's circumference to its diameter.",
                "volume": "Volume measures how much space a 3D shape occupies, measured in cubic units.",
                "area": "Area measures the space inside a 2D shape, measured in square units."
            }
        }
        
        self.greetings = [
            "Hello! I'm your geometry tutor. How can I help you today?",
            "Hi there! Ready to learn some geometry?",
            "Welcome! I'm here to help with shapes, formulas, and geometry concepts.",
            "Greetings! Ask me anything about geometric shapes."
        ]
        
        self.encouragements = [
            "Great question!",
            "That's an interesting topic!",
            "Let me explain that for you.",
            "I can help with that!"
        ]
    
    def get_response(self, message, user_id):
        """Generate a response to user message"""
        message_lower = message.lower()
        
        # Check for greetings
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greetings)
        
        # Check for shape-specific questions
        for shape in ["cube", "sphere", "cone", "cylinder", "triangle", "rectangle"]:
            if shape in message_lower:
                for topic in ["volume", "surface", "area", "perimeter", "what is", "explain", "describe"]:
                    if topic in message_lower:
                        if shape in self.knowledge_base and topic in self.knowledge_base[shape]:
                            encouragement = random.choice(self.encouragements)
                            return f"{encouragement} {self.knowledge_base[shape][topic]}"
                
                # General shape description
                if shape in self.knowledge_base:
                    return f"{self.knowledge_base[shape]['description']} What specifically would you like to know about {shape}s?"
        
        # Check for general topics
        for topic in self.knowledge_base["general"]:
            if topic in message_lower:
                return self.knowledge_base["general"][topic]
        
        # Check for formula questions
        if any(word in message_lower for word in ["formula", "calculate", "compute", "find"]):
            if "volume" in message_lower:
                return "For volume formulas: Cube = a³, Sphere = 4/3 π r³, Cone = (1/3) π r² h, Cylinder = π r² h"
            elif "surface" in message_lower or "area" in message_lower:
                return "For surface area: Cube = 6a², Sphere = 4πr², Cylinder = 2πr(h + r)"
            elif "perimeter" in message_lower:
                return "For perimeter: Rectangle = 2(length + width), Triangle = sum of all sides"
        
        # Default response
        return "I can help you with geometry concepts, formulas for shapes (cube, sphere, cone, cylinder, triangle, rectangle), and calculations. Try asking about a specific shape or formula!"
    
    def get_quiz_feedback(self, score, total):
        """Provide feedback based on quiz performance"""
        percentage = (score / total) * 100
        
        if percentage >= 90:
            return "Excellent work! You have a strong understanding of geometric shapes and formulas."
        elif percentage >= 70:
            return "Good job! You understand most concepts well. Keep practicing!"
        elif percentage >= 50:
            return "Not bad! You're getting there. Review the shapes section and try the practice exercises."
        else:
            return "Let's review the basics together. Check out the shapes section and don't hesitate to ask me questions!"
    
    def get_practice_feedback(self, correct, total, exercises):
        """Provide feedback on practice exercises"""
        percentage = (correct / total) * 100
        
        if percentage == 100:
            return "Perfect score! You've mastered these exercises. Ready for more challenging problems?"
        elif percentage >= 80:
            return "Great work! You understand these concepts well."
        elif percentage >= 60:
            return "Good effort! You're on the right track. Review any mistakes and try again."
        else:
            # Identify weak areas
            weak_areas = []
            if len(exercises) >= 5:
                if exercises[0].get("correct") == False:
                    weak_areas.append("cube volume")
                if exercises[1].get("correct") == False:
                    weak_areas.append("sphere surface area")
                if exercises[2].get("correct") == False:
                    weak_areas.append("triangle area")
                if exercises[3].get("correct") == False:
                    weak_areas.append("cylinder volume")
                if exercises[4].get("correct") == False:
                    weak_areas.append("rectangle perimeter")
            
            if weak_areas:
                return f"Let's focus on: {', '.join(weak_areas)}. Review these formulas and try again!"
            else:
                return "Keep practicing! Each attempt helps you learn. Don't hesitate to ask me for help with specific formulas."