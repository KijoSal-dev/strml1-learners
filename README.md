# strml1-learners
# AI Tutor for Special Needs Learners

## Project Overview

AI Tutor for Special Needs Learners is an interactive, accessible, and personalized educational platform built with Streamlit. It is designed to support children with special learning needs by providing tailored lessons, quizzes, games, and progress tracking in a safe and engaging environment.

## Key Features

- User authentication and personalized profiles
- Adaptive learning activities for Math, Reading, Social Skills, Science, and Creative Arts
- Practice quizzes with instant feedback
- Fun educational games
- Progress tracking and achievement badges
- Accessibility controls (text-to-speech, high contrast, large text)
- AI-powered chat tutor for guidance and encouragement
- Data export and user settings management

## Project Implementation Steps

### 1. Define Problem and Scope

- **Problem:** Many children with special needs lack access to personalized, adaptive, and accessible digital learning tools.
- **Scope:** Build a web-based platform that adapts content and interaction to individual learning needs and preferences.
- **Objectives:** 
  - Deliver engaging, accessible, and adaptive learning experiences.
  - Track progress and provide feedback.
  - Support a variety of learning styles and needs.
- **Target Users:** Children with special learning needs, their parents, and educators.
- **Key Metrics:** User engagement, learning session completion, quiz scores, progress improvement, and user satisfaction.

### 2. Data Collection

- **Data Sources:** 
  - User input and interaction data (progress, quiz results, preferences).
  - Predefined educational content templates.
- **Data Preprocessing:** 
  - Clean and validate user input.
  - Structure and store session and progress data in SQLite.
- **Model Selection:** 
  - Rule-based content adaptation and quiz generation.
  - (Optional) Integrate ML/NLP models for advanced personalization.
- **Model Training and Evaluation:** 
  - Not applicable for current rule-based version.
  - Future versions may include model training for adaptive content.

### 3. Build User Interface

- Use Streamlit to create an intuitive, accessible, and visually appealing UI.
- Implement navigation, forms, dashboards, and interactive components.
- Add accessibility features (TTS, high contrast, large text).

### 4. Deployment

- Package the app with requirements.txt.
- Deploy on Streamlit Cloud, Heroku, or a similar platform.
- Ensure database file (`ai_tutor.db`) is properly initialized.

### 5. Testing and Validation

- Test user registration, login, and session flows.
- Validate learning activities, quizzes, and games.
- Check accessibility features and data export.
- Collect feedback from target users for improvements.

### 6. Documentation and Reporting

- **Handle Challenges:** 
  - Address accessibility, engagement, and personalization.
  - Ensure data privacy and security.
- **Expected Outcomes:** 
  - Improved learning engagement and outcomes for special needs learners.
  - Positive feedback from users and educators.
- **Why the Project:** 
  - To bridge the gap in accessible, adaptive digital education for children with special needs, empowering them to learn at their own pace and style.

### 7. Running the App
Start the streamlit app with:

### python -m streamlit run app.py

This will open the app in the web broswer.


### 8. Screenshots of the App

Below are some screenshots showcasing different parts of the AI Tutor for Special Needs Learners application:

- **Register Page:** User registration interface for new learners , other and no specific needs.
- **Login Page:** Secure login screen for returning users.
- **Learning Activities Page:** Interactive and adaptive learning modules tailored to user needs.
- **Fun Games Page:** Engaging educational games to reinforce learning in a playful way.
- **Dashboard Page:** Visual progress tracking, achievements, and session summaries.
- **AI Tutor Page:** Chat-based AI tutor providing guidance, encouragement, and support.

```
   ![Register Page](screenshots\Registration page.png)
   ![Login page](screenshots\Login page.png)
   ![Learning Page](screenshots\Learning activities page.png)
   ![Fun games page](screenshots\Fun games page.png)
   ![Dashboard Page](screenshots\Dashboard page.png)
   ![AI tutor page](screenshots\AI tutor page.png)
   
   ```
---

