# AstroDesk 🌌🚀

**Coders Club Hackathon 2025 Submission**  
**Theme Category: Space & Beyond**  

AstroDesk is a Python Flask-based web application that allows users to:  
- Track Near-Earth Objects (Asteroids, Comets) using NASA APIs  
- View Upcoming Space Events like Rocket Launches  
- Get the Latest Space-Related News  

---

## 🌟 Features

- **Asteroid Tracker:**  
  Real-time asteroid data using NASA NeoWs API.

- **Space Events Calendar:**  
  Upcoming launches and space events via Launch Library 2 API.

- **Space News Feed:**  
  Latest articles from Spaceflight News API.

- **Simple, Responsive UI:**  
  Built with Flask templates and Bootstrap 5.

- **Space Utilities (Weight Calculator):**  
  Calculate your weight on different planets and moons.


---

## 🔧 Tech Stack

- Python 3  
- Flask  
- Requests  
- Bootstrap 5  
- NASA APIs  
- Spaceflight News API  
- Launch Library 2 API  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository:

git clone https://github.com/JosephJonathanFernandes/astrodesk.git


cd astrodesk

### 2️⃣ Install Python Dependencies:

pip install -r requirements.txt

### 3️⃣ Set Your NASA API Key:

Open app.py

Replace:

NASA_API_KEY = "YOUR_API_KEY"

Get your key from: https://api.nasa.gov/

### 4️⃣ Run the Flask App:

python app.py

Open in browser:

http://127.0.0.1:5000

### 🗂️ Project Structure

astrodesk/
├── app.py

├── requirements.txt

├── templates/

│   ├── index.html

│   ├── asteroids.html

│   ├── news.html

│   ├── events.html

│   ├── utilities.html

│   ├── error.html

├── static/ (optional)

### 🎯 APIs Used

NASA NeoWs API

Launch Library 2 API

Spaceflight News API

### 👥 Team Members

Pratik

Akaash

Joseph

### 📄 License

For educational and hackathon use only.

All API content belongs to respective organizations.
