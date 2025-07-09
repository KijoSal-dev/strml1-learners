import streamlit as st
import requests
import json
import time
import random
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os
from typing import Dict, List, Optional
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Tutor for Special Needs Learners",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for accessibility and better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .learning-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
    
    .accessibility-controls {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .high-contrast {
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    .large-text {
        font-size: 1.2em !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Database setup
def init_database():
    conn = sqlite3.connect('ai_tutor.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            learning_needs TEXT,
            preferences TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Learning sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            activity_type TEXT,
            score INTEGER,
            duration INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Progress tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            skill TEXT,
            level INTEGER DEFAULT 1,
            points INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_database()

# Free API configurations
class FreeAPIs:
    @staticmethod
    def get_educational_content(topic: str, difficulty: str = "beginner") -> Dict:
        """Simulate educational content generation using free APIs"""
        # In a real implementation, you could use:
        # - OpenAI's free tier
        # - Hugging Face Inference API
        # - Google's Gemini API free tier
        
        content_templates = {
    "math": {
        "beginner": {
            "title": f"Fun with Numbers: {topic}",
            "content": f"Welcome to our exciting math adventure! Today we're exploring {topic}. Math is like solving puzzles - each number has a special place and purpose. We'll use colorful pictures, fun stories, and hands-on activities to make learning enjoyable and easy to understand.",
            "activities": [
                "Count colorful objects in fun pictures (toys, animals, fruits)",
                "Match numbers with the right amount of items using drag-and-drop",
                "Simple addition using virtual manipulatives and counting bears",
                "Number recognition games with audio pronunciation",
                "Create number stories with picture sequences",
                "Practice writing numbers in sand trays or finger painting",
                "Sing counting songs and number rhymes"
            ],
            "tips": "Remember: Use your fingers, toys, or snacks to count along! Take breaks when you need them, and celebrate every small success. Math is everywhere - count steps, toys, or cookies!",
            "visual_aids": ["Number charts with pictures", "Counting manipulatives", "Interactive number line"],
            "assessment": "Simple counting exercises and number recognition tasks"
        },
        "intermediate": {
            "title": f"Math Adventures: {topic}",
            "content": f"Great job learning the basics! Now we're ready for more exciting math challenges with {topic}. We'll solve real-world problems, discover patterns, and use math in everyday situations. Remember, every mathematician started exactly where you are now!",
            "activities": [
                "Solve story-based word problems with visual clues",
                "Discover and create number patterns using colors and shapes",
                "Mental math games with timer challenges (optional pressure)",
                "Real-world math: shopping, cooking, time-telling activities",
                "Geometry exploration with shape hunts and building blocks",
                "Measurement activities using rulers, scales, and measuring cups",
                "Math puzzles and brain teasers with multiple solution paths"
            ],
            "tips": "Break big problems into smaller steps. Draw pictures or diagrams to help visualize. It's okay to use calculators for complex calculations - focus on understanding the process!",
            "visual_aids": ["Problem-solving flowcharts", "Interactive graphs", "Virtual manipulatives"],
            "assessment": "Multi-step problems and practical application tasks"
        },
        "advanced": {
            "title": f"Math Mastery: {topic}",
            "content": f"You're becoming a math expert! Let's tackle advanced {topic} concepts and prepare for real-world applications. We'll explore complex problems and develop critical thinking skills.",
            "activities": [
                "Multi-step problem solving with real-world scenarios",
                "Advanced pattern recognition and algebraic thinking",
                "Data analysis and interpretation exercises",
                "Geometric proofs and spatial reasoning challenges",
                "Mathematical modeling of everyday situations",
                "Collaborative problem-solving projects"
            ],
            "tips": "Focus on understanding concepts rather than memorizing. Explain your thinking process out loud. Mistakes are learning opportunities!",
            "visual_aids": ["Advanced graphing tools", "3D modeling software", "Statistical charts"],
            "assessment": "Complex problem-solving and project-based evaluations"
        }
    },
    "reading": {
        "beginner": {
            "title": f"Reading Magic: {topic}",
            "content": f"Welcome to the wonderful world of reading! Today we'll discover {topic} through colorful pictures, simple words, and exciting stories. Reading is like having a superpower - it lets you travel to amazing places and meet incredible characters without leaving your seat!",
            "activities": [
                "Interactive picture-word matching games with audio support",
                "Letter sound practice with fun phonics songs and animations",
                "Simple sentence reading with highlighting and pacing tools",
                "Story prediction using picture clues and context",
                "Rhyming games and word family activities",
                "Sight word recognition through repetitive, engaging exercises",
                "Interactive story creation with picture prompts",
                "Reading along with audio books and following text highlighting"
            ],
            "tips": "Point to each word as you read. Sound out letters slowly and blend them together. If you get stuck on a word, look at the pictures for clues. Reading gets easier with practice!",
            "visual_aids": ["Picture books with large text", "Interactive phonics charts", "Word-picture association cards"],
            "assessment": "Letter recognition, simple word reading, and picture comprehension"
        },
        "intermediate": {
            "title": f"Story Adventures: {topic}",
            "content": f"You're becoming a confident reader! Let's dive into exciting stories about {topic} and expand our vocabulary. We'll explore different types of texts, learn new words, and develop reading strategies that will help you understand any book you pick up.",
            "activities": [
                "Read engaging short stories and chapter books with discussion",
                "Answer comprehension questions using text evidence",
                "Vocabulary building through context clues and word games",
                "Character analysis and story element identification",
                "Reading different genres: fiction, non-fiction, poetry",
                "Making predictions and inferences about story outcomes",
                "Summarizing stories in your own words",
                "Creative writing inspired by reading materials"
            ],
            "tips": "Use context clues when you encounter new words. Ask yourself questions while reading: Who? What? Where? When? Why? Reread parts that don't make sense.",
            "visual_aids": ["Graphic organizers", "Story maps", "Vocabulary journals"],
            "assessment": "Reading comprehension, vocabulary usage, and story analysis"
        },
        "advanced": {
            "title": f"Literary Exploration: {topic}",
            "content": f"Welcome to advanced reading! We'll analyze complex texts about {topic}, explore literary devices, and develop critical thinking skills. You're ready to tackle challenging materials and express sophisticated ideas.",
            "activities": [
                "Analyze complex texts and literary themes",
                "Compare and contrast different authors' perspectives",
                "Research projects using multiple sources",
                "Creative writing with advanced techniques",
                "Book discussions and literary criticism",
                "Poetry analysis and interpretation"
            ],
            "tips": "Take notes while reading. Look for themes and deeper meanings. Discuss your ideas with others to gain new perspectives.",
            "visual_aids": ["Literary analysis frameworks", "Research databases", "Writing templates"],
            "assessment": "Literary analysis, research projects, and creative writing portfolios"
        }
    },
    "social": {
        "beginner": {
            "title": f"Friendship Skills: {topic}",
            "content": f"Learning about {topic} helps us make friends and get along with others! Social skills are like tools in a toolbox - the more we practice using them, the better we become at building friendships and solving problems with others. Everyone learns at their own pace, and that's perfectly okay!",
            "activities": [
                "Fun role-playing scenarios with puppets and props",
                "Emotion recognition games using facial expressions and body language",
                "Practice conversations with guided prompts and visual cues",
                "Turn-taking games and sharing activities",
                "Problem-solving scenarios with multiple solutions",
                "Empathy building through story characters and situations",
                "Non-verbal communication practice (gestures, personal space)",
                "Conflict resolution using 'I feel' statements and compromise"
            ],
            "tips": "Practice these skills with family first, then try with friends. It's okay to make mistakes - that's how we learn! Use your words to express feelings instead of actions.",
            "visual_aids": ["Emotion cards and charts", "Social story books", "Video modeling examples"],
            "assessment": "Role-play demonstrations and social situation responses"
        },
        "intermediate": {
            "title": f"Social Navigation: {topic}",
            "content": f"You're developing great social skills! Now let's explore more complex social situations involving {topic}. We'll learn about different social contexts, cultural awareness, and advanced communication strategies.",
            "activities": [
                "Complex social scenario problem-solving",
                "Group project collaboration and leadership skills",
                "Cultural awareness and diversity appreciation",
                "Advanced conflict resolution and mediation",
                "Public speaking and presentation skills",
                "Digital citizenship and online social skills",
                "Community involvement and service learning"
            ],
            "tips": "Listen actively to others. Consider different perspectives before responding. Practice assertiveness while remaining respectful.",
            "visual_aids": ["Social situation flowcharts", "Cultural diversity resources", "Communication style guides"],
            "assessment": "Group projects, presentation skills, and peer interaction evaluations"
        },
        "advanced": { # Added missing 'advanced' level for social
            "title": f"Community Leadership: {topic}",
            "content": f"You're ready to lead! Let's explore advanced social dynamics within {topic}, focusing on leadership, advocacy, and global citizenship. You'll learn to make a positive impact on your community and beyond.",
            "activities": [
                "Organize and lead group discussions on social issues",
                "Develop and present proposals for community improvement",
                "Participate in mock debates or forums",
                "Explore global social challenges and solutions",
                "Mentor younger peers in social skills",
                "Analyze and discuss current events with a social lens"
            ],
            "tips": "Lead by example. Encourage open dialogue and diverse viewpoints. Remember that true leadership is about serving others.",
            "visual_aids": ["Leadership frameworks", "Global issues maps", "Debate guidelines"],
            "assessment": "Leadership role-play, community project proposals, and persuasive presentations"
        }
    },
    "science": {
        "beginner": {
            "title": f"Science Discoveries: {topic}",
            "content": f"Welcome to the amazing world of science! Today we'll explore {topic} through hands-on experiments and observations. Science is all around us - from the air we breathe to the plants that grow. Let's become science detectives and discover how things work!",
            "activities": [
                "Simple experiments with everyday materials",
                "Nature observations and data collection",
                "Interactive science simulations and virtual labs",
                "Science vocabulary building with visual associations",
                "Hypothesis formation and testing",
                "Science journal keeping with drawings and observations"
            ],
            "tips": "Ask lots of questions! Science is about curiosity. Make predictions before experiments and observe carefully.",
            "visual_aids": ["Science experiment videos", "Interactive diagrams", "Nature identification guides"],
            "assessment": "Experiment observations and simple scientific explanations"
        },
        "intermediate": { # Added missing 'intermediate' level for science
            "title": f"Scientific Explorations: {topic}",
            "content": f"Great job with basic science! Now let's delve deeper into {topic} with more complex experiments and critical thinking. We'll learn how to design experiments, interpret data, and understand scientific principles.",
            "activities": [
                "Design and conduct controlled experiments",
                "Analyze and graph experimental data",
                "Research and present on scientific topics",
                "Explore the scientific method in detail",
                "Dissect simple organisms (virtual or actual)",
                "Build simple models (e.g., solar system, cell)"
            ],
            "tips": "Formulate clear hypotheses. Control variables in experiments. Document your findings thoroughly and logically.",
            "visual_aids": ["Scientific method charts", "Data analysis software", "Microscope images"],
            "assessment": "Experimental reports, scientific presentations, and data interpretation tasks"
        },
        "advanced": { # Added missing 'advanced' level for science
            "title": f"Advanced Scientific Inquiry: {topic}",
            "content": f"You're a true scientist! Let's tackle advanced concepts in {topic}, engage in in-depth research, and develop innovative solutions to scientific problems. Prepare to contribute to scientific understanding.",
            "activities": [
                "Conduct independent research projects",
                "Engage in complex scientific debates",
                "Utilize advanced scientific instruments (simulated or real)",
                "Develop solutions to environmental or health challenges",
                "Participate in science fairs or competitions",
                "Write and present scientific papers"
            ],
            "tips": "Critically evaluate sources. Collaborate with peers on complex problems. Don't be afraid to challenge existing ideas with evidence.",
            "visual_aids": ["Research databases", "Advanced simulation software", "Peer-reviewed journals"],
            "assessment": "Research projects, scientific presentations, and peer-reviewed articles"
        }
    },
    "creative": {
        "beginner": {
            "title": f"Creative Expression: {topic}",
            "content": f"Let's unleash your creativity with {topic}! Art and creativity help us express our feelings, tell stories, and see the world in new ways. There's no right or wrong way to be creative - your unique perspective is what makes your art special!",
            "activities": [
                "Multi-sensory art projects using various materials",
                "Storytelling through visual art and drama",
                "Music and movement activities",
                "Creative writing and poetry",
                "Digital art and multimedia projects",
                "Collaborative art installations"
            ],
            "tips": "Express yourself freely! There are no mistakes in art, only discoveries. Try different materials and techniques.",
            "visual_aids": ["Art technique tutorials", "Creative inspiration galleries", "Step-by-step project guides"],
            "assessment": "Creative portfolios and self-reflection on artistic choices"
        },
        "intermediate": { # Added missing 'intermediate' level for creative
            "title": f"Artistic Journeys: {topic}",
            "content": f"You're growing as an artist! Let's explore diverse art forms related to {topic} and refine your creative skills. We'll learn about artistic elements, principles of design, and different creative processes.",
            "activities": [
                "Explore different art mediums (painting, sculpture, digital)",
                "Learn about famous artists and their styles",
                "Develop original stories, poems, or scripts",
                "Compose simple musical pieces or rhythms",
                "Design and create wearable art or functional objects",
                "Collaborate on a group performance piece"
            ],
            "tips": "Experiment with different styles. Seek inspiration from your surroundings. Practice regularly to hone your craft.",
            "visual_aids": ["Art history timelines", "Music composition software", "Design principles guides"],
            "assessment": "Art projects demonstrating technique, creative writing portfolios, and performance participation"
        },
        "advanced": { # Added missing 'advanced' level for creative
            "title": f"Mastering Creativity: {topic}",
            "content": f"You're truly mastering creative expression! Let's push the boundaries of {topic}, engage in advanced artistic techniques, and develop your unique artistic voice. Your creativity can inspire and influence others.",
            "activities": [
                "Undertake complex, multi-medium art projects",
                "Produce and direct short films or theatrical scenes",
                "Compose original songs or musical scores",
                "Curate a personal art exhibition or digital portfolio",
                "Participate in creative writing workshops and critique sessions",
                "Explore the intersection of art and technology"
            ],
            "tips": "Develop a strong personal vision. Seek constructive criticism to improve. Don't be afraid to take risks and innovate.",
            "visual_aids": ["Advanced artistic software", "Filmmaking tutorials", "Music theory resources"],
            "assessment": "Major creative projects, public performances, and critical reviews of artistic work"
        }
    }
}
        
def get_content_template(topic, difficulty, content_templates):
    subject = topic.lower()
    if "math" in subject or "number" in subject or "counting" in subject:
        return content_templates["math"][difficulty]
    elif "read" in subject or "story" in subject or "book" in subject:
        return content_templates["reading"][difficulty]
    elif "social" in subject or "friend" in subject or "emotion" in subject:
        return content_templates["social"][difficulty]
    elif "science" in subject or "experiment" in subject or "nature" in subject:
        return content_templates["science"][difficulty]
    elif "art" in subject or "creative" in subject or "music" in subject:
        return content_templates["creative"][difficulty]
    else:
        return content_templates["reading"][difficulty]

# Example usage (assuming content_templates exists)
# my_templates = {"math": {"easy": "1+1=?", "medium": "2*X=10"}, "reading": {"easy": "Cat sat on mat."}}
# template = get_content_template("math", "easy", my_templates)
# print(template)
       
    @staticmethod
    def text_to_speech_url(text: str) -> str:
        """Generate text-to-speech using free APIs"""
        # Using ResponsiveVoice (free tier)
        # In production, you might use Google Cloud TTS free tier or Amazon Polly
        encoded_text = requests.utils.quote(text)
        return f"https://responsivevoice.org/responsivevoice/getvoice.php?t={encoded_text}&tl=en&sv=g1&vn=&pitch=0.5&rate=0.5&vol=1"
    
    @staticmethod
    def generate_quiz_questions(topic: str, difficulty: str = "beginner") -> List[Dict]:
        """Generate quiz questions based on topic and difficulty"""
        quiz_templates = {
            "math": {
                "beginner": [
                    {
                        "question": "What comes after the number 5?",
                        "options": ["4", "6", "7", "3"],
                        "correct": 1,
                        "explanation": "When counting: 1, 2, 3, 4, 5, 6... So 6 comes after 5!"
                    },
                    {
                        "question": "How many apples are there? 🍎🍎🍎",
                        "options": ["2", "3", "4", "5"],
                        "correct": 1,
                        "explanation": "Count them: 1, 2, 3 apples!"
                    }
                ],
                "intermediate": [
                    {
                        "question": "What is 7 + 3?",
                        "options": ["9", "10", "11", "8"],
                        "correct": 1,
                        "explanation": "7 + 3 = 10. You can count: 7, 8, 9, 10!"
                    }
                ]
            },
            "reading": {
                "beginner": [
                    {
                        "question": "What sound does the letter 'B' make?",
                        "options": ["Buh", "Duh", "Guh", "Puh"],
                        "correct": 0,
                        "explanation": "The letter B makes the 'Buh' sound, like in 'Ball' or 'Book'!"
                    }
                ],
                "intermediate": [
                    {
                        "question": "What is the main character in a story called?",
                        "options": ["Villain", "Hero", "Protagonist", "Author"],
                        "correct": 2,
                        "explanation": "The protagonist is the main character that the story follows!"
                    }
                ]
            }
        }
        
        subject = "math" if "math" in topic.lower() else "reading"
        return quiz_templates.get(subject, {}).get(difficulty, quiz_templates["reading"]["beginner"])

# User authentication functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str, name: str, age: int, learning_needs: str, preferences: str) -> bool:
    try:
        conn = sqlite3.connect('ai_tutor.db')
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password_hash, name, age, learning_needs, preferences)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, name, age, learning_needs, preferences))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    conn = sqlite3.connect('ai_tutor.db')
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
        SELECT id, username, name, age, learning_needs, preferences
        FROM users WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'name': user[2],
            'age': user[3],
            'learning_needs': user[4],
            'preferences': user[5]
        }
    return None

def save_learning_session(user_id: int, subject: str, activity_type: str, score: int, duration: int):
    conn = sqlite3.connect('ai_tutor.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO learning_sessions (user_id, subject, activity_type, score, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, subject, activity_type, score, duration))
    
    conn.commit()
    conn.close()

def update_progress(user_id: int, subject: str, skill: str, points: int):
    conn = sqlite3.connect('ai_tutor.db')
    cursor = conn.cursor()
    
    # Check if progress record exists
    cursor.execute('''
        SELECT id, points, level FROM progress 
        WHERE user_id = ? AND subject = ? AND skill = ?
    ''', (user_id, subject, skill))
    
    existing = cursor.fetchone()
    
    if existing:
        new_points = existing[1] + points
        new_level = existing[2] + (1 if new_points >= existing[2] * 100 else 0)
        
        cursor.execute('''
            UPDATE progress SET points = ?, level = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_points, new_level, existing[0]))
    else:
        cursor.execute('''
            INSERT INTO progress (user_id, subject, skill, points)
            VALUES (?, ?, ?, ?)
        ''', (user_id, subject, skill, points))
    
    conn.commit()
    conn.close()

def get_user_progress(user_id: int) -> List[Dict]:
    conn = sqlite3.connect('ai_tutor.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT subject, skill, level, points FROM progress WHERE user_id = ?
    ''', (user_id,))
    
    progress = cursor.fetchall()
    conn.close()
    
    return [{'subject': p[0], 'skill': p[1], 'level': p[2], 'points': p[3]} for p in progress]

# Accessibility features
def render_accessibility_controls():
    st.markdown('<div class="accessibility-controls">', unsafe_allow_html=True)
    st.subheader("🔧 Accessibility Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Read Aloud"):
            st.session_state.read_aloud = True
            st.success("Text-to-speech enabled!")
    
    with col2:
        if st.button("🎨 High Contrast"):
            st.session_state.high_contrast = not st.session_state.get('high_contrast', False)
            st.success("High contrast toggled!")
    
    with col3:
        if st.button("📝 Large Text"):
            st.session_state.large_text = not st.session_state.get('large_text', False)
            st.success("Large text toggled!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main application
def main():
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    # Header
    st.markdown('''
    <div class="main-header">
        <h1>🎓 AI Tutor for Special Needs Learners</h1>
        <p>Personalized learning experiences designed for every unique learner</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Accessibility controls
    render_accessibility_controls()
    
    # Authentication
    if st.session_state.user is None:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Welcome Back! 👋")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", key="login_btn"):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            st.subheader("Join Our Learning Community! 🌟")
            
            col1, col2 = st.columns(2)
            with col1:
                reg_name = st.text_input("Full Name", key="reg_name")
                reg_username = st.text_input("Username", key="reg_username")
                reg_password = st.text_input("Password", type="password", key="reg_password")
            
            with col2:
                reg_age = st.number_input("Age", min_value=3, max_value=100, value=10, key="reg_age")
                learning_needs = st.selectbox("Learning Needs", [
                    "Autism Spectrum Disorder",
                    "ADHD",
                    "Dyslexia",
                    "Intellectual Disability",
                    "Down Syndrome",
                    "Cerebral Palsy",
                    "Other",
                    "No specific needs"
                ], key="reg_needs")
                
                preferences = st.multiselect("Learning Preferences", [
                    "Visual Learning",
                    "Audio Learning",
                    "Hands-on Activities",
                    "Repetition",
                    "Short Sessions",
                    "Gamification",
                    "Social Learning"
                ], key="reg_prefs")
            
            if st.button("Create Account", key="register_btn"):
                if reg_name and reg_username and reg_password:
                    if create_user(reg_username, reg_password, reg_name, reg_age, learning_needs, json.dumps(preferences)):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists. Please choose a different one.")
                else:
                    st.error("Please fill in all required fields.")
    
    else:
        # Main application for logged-in users
        user = st.session_state.user
        
        # Sidebar navigation
        st.sidebar.title(f"Hello, {user['name']}! 👋")
        st.sidebar.markdown(f"**Age:** {user['age']}")
        st.sidebar.markdown(f"**Learning Focus:** {user['learning_needs']}")
        
        page = st.sidebar.selectbox("Navigate to:", [
            "🏠 Dashboard",
            "📚 Learning Activities",
            "🎯 Practice Quiz",
            "📈 My Progress",
            "🎮 Fun Games",
            "👨‍🏫 AI Tutor Chat",
            "⚙️ Settings"
        ])
        
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
        
        # Main content based on selected page
        if page == "🏠 Dashboard":
            render_dashboard(user)
        elif page == "📚 Learning Activities":
            render_learning_activities(user)
        elif page == "🎯 Practice Quiz":
            render_quiz_section(user)
        elif page == "📈 My Progress":
            render_progress_section(user)
        elif page == "🎮 Fun Games":
            render_games_section(user)
        elif page == "👨‍🏫 AI Tutor Chat":
            render_ai_tutor_chat(user)
        elif page == "⚙️ Settings":
            render_settings(user)

def render_dashboard(user):
    st.header("📊 Your Learning Dashboard")
    
    # Welcome message
    current_time = datetime.now().hour
    if current_time < 12:
        greeting = "Good morning"
    elif current_time < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    st.markdown(f"### {greeting}, {user['name']}! Ready to learn something amazing today? 🌟")
    
    # Progress overview
    progress_data = get_user_progress(user['id'])
    
    if progress_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_points = sum(p['points'] for p in progress_data)
            st.metric("Total Points", total_points, "🏆")
        
        with col2:
            avg_level = sum(p['level'] for p in progress_data) / len(progress_data)
            st.metric("Average Level", f"{avg_level:.1f}", "📈")
        
        with col3:
            subjects_count = len(set(p['subject'] for p in progress_data))
            st.metric("Subjects Learning", subjects_count, "📚")
    
    # Quick actions
    st.subheader("🚀 Quick Start")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 Start Reading", use_container_width=True):
            st.session_state.current_lesson = "reading"
            st.success("Let's read together! 📚")
    
    with col2:
        if st.button("🔢 Practice Math", use_container_width=True):
            st.session_state.current_lesson = "math"
            st.success("Math time! Let's count! 🧮")
    
    with col3:
        if st.button("👥 Social Skills", use_container_width=True):
            st.session_state.current_lesson = "social"
            st.success("Let's learn about feelings! 😊")
    
    # Recent achievements
    if progress_data:
        st.subheader("🏅 Recent Achievements")
        for progress in progress_data[-3:]:  # Show last 3
            st.markdown(f"""
            <div class="achievement-badge">
                Level {progress['level']} in {progress['subject']} - {progress['skill']}
            </div>
            """, unsafe_allow_html=True)

def render_learning_activities(user):
    st.header("📚 Learning Activities")
    
    # Subject selection
    subject = st.selectbox("Choose a subject:", [
        "Reading & Language",
        "Mathematics",
        "Social Skills",
        "Science Basics",
        "Creative Arts"
    ])
    
    # Difficulty level
    difficulty = st.radio("Choose difficulty:", ["Beginner", "Intermediate"], horizontal=True)
    
    if st.button("Start Learning Session"):
        # Generate content using free APIs
        content = FreeAPIs.get_educational_content(subject, difficulty.lower())
        
        st.markdown(f"""
        <div class="learning-card">
            <h3>{content['title']}</h3>
            <p>{content['content']}</p>
            <h4>Activities:</h4>
            <ul>
        """, unsafe_allow_html=True)
        
        for activity in content['activities']:
            st.markdown(f"<li>{activity}</li>", unsafe_allow_html=True)
        
        st.markdown(f"""
            </ul>
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                <strong>💡 Tip:</strong> {content['tips']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Text-to-speech option
        if st.button("🔊 Read This Aloud"):
            tts_url = FreeAPIs.text_to_speech_url(content['content'])
            st.audio(tts_url)
        
        # Complete session
        if st.button("✅ Complete Session"):
            save_learning_session(user['id'], subject, "lesson", 100, 15)
            update_progress(user['id'], subject, "general", 10)
            st.success("Great job! Session completed! 🎉")
            st.balloons()

def render_quiz_section(user):
    st.header("🎯 Practice Quiz")
    
    if not st.session_state.quiz_started:
        st.markdown("### Ready for a fun quiz? Let's test what you've learned! 🧠")
        
        quiz_subject = st.selectbox("Choose quiz topic:", [
            "Basic Math",
            "Reading Skills",
            "Social Situations"
        ])
        
        quiz_difficulty = st.radio("Difficulty:", ["Beginner", "Intermediate"], horizontal=True)
        
        if st.button("Start Quiz! 🚀"):
            st.session_state.quiz_started = True
            st.session_state.quiz_questions = FreeAPIs.generate_quiz_questions(quiz_subject, quiz_difficulty.lower())
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
            st.rerun()
    
    else:
        questions = st.session_state.quiz_questions
        current_q = st.session_state.current_question
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(questions)}")
            st.markdown(f"**{question['question']}**")
            
            # Answer options
            answer = st.radio("Choose your answer:", question['options'], key=f"q_{current_q}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Submit Answer"):
                    if question['options'].index(answer) == question['correct']:
                        st.success("Correct! 🎉")
                        st.session_state.quiz_score += 1
                    else:
                        st.error("Not quite right, but great try! 💪")
                    
                    st.info(f"**Explanation:** {question['explanation']}")
                    
                    if current_q < len(questions) - 1:
                        if st.button("Next Question ➡️"):
                            st.session_state.current_question += 1
                            st.rerun()
                    else:
                        if st.button("Finish Quiz 🏁"):
                            st.session_state.current_question += 1
                            st.rerun()
            
            with col2:
                # Progress bar
                progress = (current_q + 1) / len(questions)
                st.progress(progress)
                st.write(f"Progress: {current_q + 1}/{len(questions)}")
        
        else:
            # Quiz completed
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100
            
            st.markdown("### 🎊 Quiz Completed!")
            st.markdown(f"**Your Score: {score}/{total} ({percentage:.0f}%)**")
            
            if percentage >= 80:
                st.success("Excellent work! You're a superstar! ⭐")
                points = 20
            elif percentage >= 60:
                st.success("Good job! Keep practicing! 👍")
                points = 15
            else:
                st.info("Great effort! Practice makes perfect! 💪")
                points = 10
            
            # Save results
            save_learning_session(user['id'], "Quiz", "assessment", score, 10)
            update_progress(user['id'], "Quiz", "problem_solving", points)
            
            if st.button("Take Another Quiz"):
                st.session_state.quiz_started = False
                st.rerun()

def render_progress_section(user):
    st.header("📈 My Learning Progress")
    
    progress_data = get_user_progress(user['id'])
    
    if progress_data:
        # Create progress visualization
        df = pd.DataFrame(progress_data)
        
        # Progress by subject
        st.subheader("📊 Progress by Subject")
        subject_progress = df.groupby('subject').agg({
            'level': 'mean',
            'points': 'sum'
        }).round(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            subject_progress['level'].plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title('Average Level by Subject')
            ax.set_ylabel('Level')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            subject_progress['points'].plot(kind='bar', ax=ax, color='lightgreen')
            ax.set_title('Total Points by Subject')
            ax.set_ylabel('Points')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Detailed progress table
        st.subheader("📋 Detailed Progress")
        st.dataframe(df, use_container_width=True)
        
        # Learning streaks and achievements
        st.subheader("🏆 Achievements")
        total_points = df['points'].sum()
        max_level = df['level'].max()
        
        achievements = []
        if total_points >= 100:
            achievements.append("🌟 Century Club - 100+ Points!")
        if max_level >= 5:
            achievements.append("🚀 Level Master - Reached Level 5!")
        if len(df['subject'].unique()) >= 3:
            achievements.append("🎓 Multi-Subject Learner!")
        
        if achievements:
            for achievement in achievements:
                st.markdown(f"""
                <div class="achievement-badge">
                    {achievement}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keep learning to unlock achievements! 🌟")
    
    else:
        st.info("Start learning to see your progress here! 📚")

def render_games_section(user):
    st.header("🎮 Fun Learning Games")
    
    game_choice = st.selectbox("Choose a game:", [
        "🔢 Number Guessing Game",
        "🎨 Color Memory Game",
        "📝 Word Building Game",
        "🧩 Pattern Matching"
    ])
    
    if game_choice == "🔢 Number Guessing Game":
        st.subheader("Guess the Number!")
        
        if 'target_number' not in st.session_state:
            st.session_state.target_number = random.randint(1, 10)
            st.session_state.guesses = 0
        
        st.write("I'm thinking of a number between 1 and 10! 🤔")
        
        guess = st.number_input("Your guess:", min_value=1, max_value=10, value=5)
        
        if st.button("Make Guess!"):
            st.session_state.guesses += 1
            
            if guess == st.session_state.target_number:
                st.success(f"🎉 Correct! You got it in {st.session_state.guesses} tries!")
                update_progress(user['id'], "Games", "number_recognition", 5)
                if st.button("Play Again"):
                    del st.session_state.target_number
                    st.rerun()
            elif guess < st.session_state.target_number:
                st.info("📈 Try a bigger number!")
            else:
                st.info("📉 Try a smaller number!")
    
    elif game_choice == "🎨 Color Memory Game":
        st.subheader("Color Memory Challenge!")
        
        colors = ["🔴 Red", "🔵 Blue", "🟢 Green", "🟡 Yellow", "🟣 Purple"]
        
        if 'color_sequence' not in st.session_state:
            st.session_state.color_sequence = random.sample(colors, 3)
            st.session_state.show_sequence = True
        
        if st.session_state.show_sequence:
            st.write("Remember this sequence:")
            st.write(" → ".join(st.session_state.color_sequence))
            
            if st.button("I've memorized it!"):
                st.session_state.show_sequence = False
                st.rerun()
        else:
            st.write("What was the sequence?")
            user_sequence = []
            
            for i in range(3):
                color = st.selectbox(f"Color {i+1}:", colors, key=f"color_{i}")
                user_sequence.append(color)
            
            if st.button("Check Answer"):
                if user_sequence == st.session_state.color_sequence:
                    st.success("🎉 Perfect memory! Well done!")
                    update_progress(user['id'], "Games", "memory", 8)
                else:
                    st.error("Not quite right. Try again! 💪")
                
                if st.button("New Game"):
                    del st.session_state.color_sequence
                    st.rerun()

def render_ai_tutor_chat(user):
    st.header("👨‍🏫 Chat with Your AI Tutor")
    
    st.markdown("""
    ### Hi there! I'm your AI learning buddy! 🤖
    
    Ask me anything about:
    - 📚 Help with lessons
    - 🤔 Explaining difficult concepts
    - 🎯 Learning tips and strategies
    - 😊 Encouragement and motivation
    """)
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI Tutor:** {message['content']}")
    
    # User input
    user_input = st.text_input("Ask me anything:", key="chat_input")
    
    if st.button("Send") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        # Generate AI response (simplified for demo)
        ai_response = generate_ai_response(user_input, user)
        st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
        
        st.rerun()

def generate_ai_response(user_input: str, user: Dict) -> str:
    """Generate AI tutor response based on user input"""
    input_lower = user_input.lower()
    
    # Simple rule-based responses (in production, use actual AI APIs)
    if any(word in input_lower for word in ['help', 'stuck', 'difficult', 'hard']):
        return f"I understand this might be challenging, {user['name']}! Remember, every expert was once a beginner. Let's break this down into smaller steps. What specific part would you like help with? 🤗"
    
    elif any(word in input_lower for word in ['math', 'number', 'count']):
        return "Math can be fun! 🔢 Try using objects around you to count, or draw pictures to help visualize problems. Would you like me to create a simple math exercise for you?"
    
    elif any(word in input_lower for word in ['read', 'book', 'story']):
        return "Reading opens up amazing worlds! 📚 Start with books that have lots of pictures, and don't worry about reading every word perfectly. The most important thing is to enjoy the story! What kind of stories do you like?"
    
    elif any(word in input_lower for word in ['sad', 'frustrated', 'angry', 'upset']):
        return f"It's okay to feel that way sometimes, {user['name']}. Learning can be challenging, but you're doing great! Take a deep breath, maybe take a short break, and remember that I'm here to help you. You've got this! 💪😊"
    
    elif any(word in input_lower for word in ['good', 'great', 'awesome', 'happy']):
        return "That's wonderful to hear! 🌟 I'm so proud of your positive attitude. Keep up the great work! What would you like to learn about next?"
    
    else:
        return f"That's a great question, {user['name']}! I'm here to help you learn and grow. Can you tell me more about what you'd like to know? Remember, there are no silly questions - every question helps you learn! 🎓"

def render_settings(user):
    st.header("⚙️ Settings")
    
    st.subheader("👤 Profile Information")
    
    # Display current settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Name:** {user['name']}")
        st.info(f"**Age:** {user['age']}")
        st.info(f"**Learning Needs:** {user['learning_needs']}")
    
    with col2:
        preferences = json.loads(user['preferences']) if user['preferences'] else []
        st.info(f"**Learning Preferences:** {', '.join(preferences) if preferences else 'None set'}")
    
    st.subheader("🎨 Appearance Settings")
    
    # Theme settings
    theme = st.selectbox("Choose theme:", ["Default", "High Contrast", "Large Text", "Colorful"])
    
    if st.button("Apply Theme"):
        st.success(f"Theme '{theme}' applied!")
    
    st.subheader("🔊 Audio Settings")
    
    # Audio preferences
    enable_sounds = st.checkbox("Enable sound effects", value=True)
    enable_tts = st.checkbox("Enable text-to-speech", value=True)
    speech_speed = st.slider("Speech speed", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("Save Audio Settings"):
        st.success("Audio settings saved!")
    
    st.subheader("📊 Learning Preferences")
    
    # Learning customization
    session_length = st.slider("Preferred session length (minutes)", 5, 30, 15)
    difficulty_preference = st.selectbox("Default difficulty:", ["Beginner", "Intermediate", "Advanced"])
    reminder_frequency = st.selectbox("Learning reminders:", ["Daily", "Every 2 days", "Weekly", "None"])
    
    if st.button("Save Learning Preferences"):
        st.success("Learning preferences saved!")
    
    st.subheader("📈 Progress & Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Progress Data"):
            progress_data = get_user_progress(user['id'])
            if progress_data:
                df = pd.DataFrame(progress_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{user['name']}_progress.csv",
                    mime="text/csv"
                )
            else:
                st.info("No progress data to export yet!")
    
    with col2:
        if st.button("🗑️ Reset All Progress"):
            if st.checkbox("I understand this will delete all my progress"):
                # In a real app, you'd implement this functionality
                st.warning("This feature is disabled in the demo for safety!")

if __name__ == "__main__":
    main()