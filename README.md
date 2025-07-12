# AstroDesk 🌌🚀

**Coders Club Hackathon 2025 Submission**  
**Theme Category: Space & Beyond**  

AstroDesk is a comprehensive Python Flask-based web application that provides an immersive space exploration experience with:  
- Track Near-Earth Objects (Asteroids, Comets) using NASA APIs  
- View Upcoming Space Events like Rocket Launches  
- Get the Latest Space-Related News  
- Interactive AI-powered Space Chat Assistant (AstroBot)  
- AI-generated Space Travel Stories with Multi-Agent Workflow  
- Advanced Space Facts with Web-sourced Verification  
- Stargazer Guide with Real-time Astronomical Data  
- Space Utilities and Calculators  
- Planet Position Visualizations  

---

## 🌟 Features

### 🌍 **Core Space Data**
- **Asteroid Tracker:**  
  Real-time near-Earth asteroid data using NASA NeoWs API with approach dates, velocities, and distances.

- **Space Events Calendar:**  
  Upcoming rocket launches and space missions via Launch Library 2 API with detailed mission information.

- **Space News Feed:**  
  Latest space exploration articles from Spaceflight News API with images and summaries.

### 🤖 **AI-Powered Features**
- **AstroBot Chat Assistant:**  
  Interactive AI chatbot powered by Groq LLM with streaming responses and space expertise.

- **Space Travel Story Generator:**  
  Multi-agent AI system that creates personalized 250-word space adventure stories with:
  - Location Feature Analysis Agent
  - Story Structure Planning Agent  
  - Creative Writing Agent
  - Quality Verification Agent
  - Dynamic mood-based storytelling (sarcastic, thrilling, wonder, etc.)

- **Intelligent Space Facts:**  
  Web-sourced space facts with multi-layer verification system:
  - Real-time fact gathering from trusted sources (Science Focus, Space.com)
  - AI fact verification for accuracy and impact
  - Iterative quality improvement with feedback loops
  - Scientific accuracy validation

### 🔭 **Astronomical Tools**
- **Stargazer Guide:**  
  Location-based sky viewing recommendations with:
  - Real-time sunrise/sunset calculations
  - Moon phase tracking
  - Celestial object visibility for major Indian cities

- **Planet Position Tracker:**  
  3D visualization of planetary positions using Skyfield astronomical calculations with enhanced UI featuring:
  - Interactive planetary position cards with detailed heliocentric coordinates
  - Real-time distance calculations from the Sun
  - Color-coded planets with astronomical symbols
  - Conversion between AU and kilometers
  - Professional data visualization with explanatory information

- **NASA Picture of the Day:**  
  Daily astronomy picture integration featuring:
  - High-resolution space imagery and videos
  - Detailed explanations and educational content
  - HD download links for wallpapers
  - Copyright attribution and professional presentation
  - Seamless integration with homepage display

- **ISS Pass Predictor:**  
  International Space Station flyover predictions for any location.

### 🛠️ **Space Utilities**
- **Planetary Weight Calculator:**  
  Calculate your weight on different planets and moons with accurate gravity factors.

- **Moon Phase Calendar:**  
  Historical and future moon phase calculations for any date.

### 🎨 **User Experience**
- **Responsive Space Theme:**  
  Custom CSS with cosmic colors, animations, and space-themed design elements.

- **Real-time Streaming:**  
  Server-sent events for live AI chat responses and data updates.

- **Interactive Navigation:**  
  Intuitive card-based interface with floating chat bot access.

- **Team Information & Credits:**  
  Comprehensive About Us section with team member profiles and project details.

- **Professional Footer:**  
  Hackathon branding with team credits and GitHub repository links.


---

## 🔧 Tech Stack

### **Backend**
- Python 3.8+  
- Flask Web Framework  
- Groq AI/LLM Integration  
- Skyfield Astronomical Library  
- Requests for API Communication  

### **Frontend**
- Bootstrap 5 Responsive Framework  
- Custom Space-themed CSS  
- Font Awesome Icons  
- Server-Sent Events (SSE) for Real-time Updates  

### **AI & Machine Learning**
- Groq Large Language Models  
- Multi-Agent AI Architecture  
- Natural Language Processing  
- Streaming Response Generation  

### **APIs & Data Sources**
- NASA APIs (NeoWs, APOD)  
- Spaceflight News API  
- Launch Library 2 API  
- Open-Notify ISS API  
- Science Focus Web Scraping  

### **Astronomical Computing**
- Skyfield for Precise Celestial Calculations  
- JPL DE421 Ephemeris Data  
- Real-time Astronomical Event Prediction  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository:

git clone https://github.com/JosephJonathanFernandes/astrodesk.git


cd astrodesk

### 2️⃣ Install Python Dependencies:

```bash
pip install flask requests groq skyfield python-dateutil
```

### 3️⃣ Set Your API Keys:

Open `app.py` and update:

```python
NASA_API_KEY = "YOUR_NASA_API_KEY"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

**Get your keys from:**
- NASA API: https://api.nasa.gov/
- Groq API: https://console.groq.com/

### 4️⃣ Download Astronomical Data:

The app will automatically download DE421 ephemeris data on first run (required for astronomical calculations).

### 5️⃣ Run the Flask App:

```bash
python app.py
```

### 6️⃣ Open in browser:

```
http://127.0.0.1:5000
```

---



The app includes:
- 🌍 **NASA Picture of the Day** on homepage
- 🤖 **AI-powered AstroBot** chat
- 🛰️ **Real-time planetary positions** with enhanced UI
- 📊 **Space data visualization** and tools
- 👥 **Team information** and project details

---

## 🗂️ Project Structure

```
astrodesk/
├── app.py                      # Main Flask application
├── workflow.py                 # AstroBot AI workflow engine
├── space_facts.py             # Multi-agent space facts generator
├── story.py                   # AI space travel story generator
├── de421.bsp                  # Astronomical ephemeris data
├── pyproject.toml             # Project dependencies
├── uv.lock                    # Dependency lock file
├── README.md                  # Project documentation
├── templates/                 # HTML templates
│   ├── index.html            # Homepage with NASA APOD and navigation cards
│   ├── about.html            # Team information and project details
│   ├── chat.html             # AI chatbot interface
│   ├── asteroids.html        # Asteroid tracking page
│   ├── news.html             # Space news feed
│   ├── events.html           # Space events calendar
│   ├── utilities.html        # Enhanced space calculation tools
│   ├── stargazer.html        # Sky viewing guide
│   ├── story.html            # AI story generator
│   ├── planet_positions_graph.html  # 3D planet visualization
│   └── error.html            # Error handling page
├── static/                   # Static assets
│   └── space-theme.css       # Custom space-themed styling
└── __pycache__/              # Python cache files
```

---

## 🎯 APIs & Data Sources Used

### **Space Data APIs**
- **NASA NeoWs API** - Near-Earth Object tracking
- **NASA APOD API** - Astronomy Picture of the Day with high-resolution imagery
- **Launch Library 2 API** - Rocket launches and missions  
- **Spaceflight News API** - Latest space news articles
- **Open-Notify ISS API** - International Space Station tracking

### **AI & Language Models**
- **Groq AI Platform** - Fast LLM inference for chat and content generation
- **Multi-Agent Architecture** - Specialized AI agents for different tasks

### **Astronomical Data**
- **JPL DE421 Ephemeris** - Precise planetary position data
- **Skyfield Library** - Professional-grade astronomical calculations
- **Science Focus** - Web-sourced verified space facts

---

## 🚀 Key Features Walkthrough

### **1. AI-Powered Chat (AstroBot)**
- Real-time streaming responses using Server-Sent Events
- Space-specialized knowledge base
- Session management for conversation context
- Professional astronomical assistance

### **2. Space Story Generator**
- Choose from 15+ cosmic destinations  
- AI analyzes location features (positive & dangerous aspects)
- Randomly selects 2 moods from 10 options (sarcastic, thrilling, wonder, etc.)
- Multi-agent workflow creates structured 250-word adventures
- Quality verification ensures engaging, accurate stories

### **3. Verified Space Facts**
- Web-scraping from trusted scientific sources
- Multi-layer fact verification system
- Impact assessment for "wow factor"
- Scientific accuracy validation
- Iterative improvement with feedback loops

### **4. Stargazer Guide**
- Real-time astronomical calculations for Indian cities
- Sunrise/sunset predictions
- Moon phase tracking with precise angles
- Optimized for amateur astronomers and sky watchers

---

## 🧠 AI Architecture

### **Multi-Agent Story Generation**
1. **Feature Analysis Agent** - Extracts destination characteristics
2. **Structure Planning Agent** - Creates mood-based story frameworks  
3. **Creative Writing Agent** - Generates engaging narratives
4. **Quality Verification Agent** - Ensures accuracy and impact

---

## 🏆 Hackathon Highlights

### **Innovation in Space Technology**
- **First-of-its-kind** multi-agent AI system for space content generation
- **Real-time astronomical calculations** integrated with web application
- **Verification-driven content** ensuring scientific accuracy
- **Immersive space experience** combining education and entertainment

### **Technical Excellence**
- **Advanced AI Architecture** with specialized agents for different tasks
- **Professional Astronomical Computing** using industry-standard libraries
- **Real-time Data Integration** from multiple space APIs
- **Responsive Design** optimized for space enthusiasts

### **Educational Impact**
- **Scientifically Accurate Content** verified through multi-layer systems
- **Interactive Learning** through AI chat and story generation
- **Practical Astronomical Tools** for real sky observation
- **Current Space Events** keeping users updated with latest developments

---

## 👥 Team AstroDesk

**Pratik Nayak** - Full Stack Developer  
**Akaash Samson** - Backend Developer  
**Joseph Jonathan Fernandes** - Frontend Developer  

Built with ❤️ at **Coders Club Hackathon 2025** by Team AstroDesk

🔗 **GitHub Repository:** https://github.com/JosephJonathanFernandes/astrodesk  

---


## 📄 License

For educational and hackathon use only.  
All API content belongs to respective organizations.  
Created for **Coders Club Hackathon 2025** - Space & Beyond Category.

---

## 🌟 Acknowledgments

- **NASA** for comprehensive space APIs
- **Groq** for high-performance AI inference
- **Skyfield** for professional astronomical calculations
- **Science Focus** for trusted space content
- **Bootstrap** for responsive design framework

**Built with ❤️ for space exploration and education**
