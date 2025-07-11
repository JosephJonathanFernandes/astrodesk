from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

NASA_API_KEY = "8gldDFCSaaAFEEsld1qYR2BAqCywsEmDCH1gkb3m"

@app.route('/')
def home():
    fun_facts = [
        "A day on Venus is longer than its year.",
        "There are more trees on Earth than stars in the Milky Way.",
        "The Moon is moving away from Earth by 3.8 cm every year.",
        "Neutron stars can spin at a rate of 600 rotations per second.",
        "One million Earths can fit inside the Sun."
    ]
    random_fact = random.choice(fun_facts)
    return render_template('index.html', fun_facts=fun_facts, random_fact=random_fact)

@app.route('/asteroids')
def asteroids():
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-07-11&api_key={NASA_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        asteroid_list = []
        for date in data['near_earth_objects']:
            for asteroid in data['near_earth_objects'][date]:
                asteroid_list.append({
                    'name': asteroid['name'],
                    'close_approach': asteroid['close_approach_data'][0]['close_approach_date'],
                    'velocity': asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                    'distance': asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                })
        return render_template('asteroids.html', asteroids=asteroid_list)
    except Exception as e:
        return render_template('error.html', message="Asteroid data not available right now.")

@app.route('/news')
def news():
    news_url = "https://api.spaceflightnewsapi.net/v4/articles"
    try:
        res = requests.get(news_url)
        articles = res.json()['results'][:10]
        return render_template('news.html', articles=articles)
    except:
        return render_template('error.html', message="Space news is currently unavailable.")

@app.route('/events')
def events():
    event_url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=5"
    try:
        res = requests.get(event_url)
        events = res.json()['results']
        return render_template('events.html', events=events)
    except:
        return render_template('error.html', message="Space events could not be fetched.")

@app.route('/utilities')
def utilities():
    return render_template('utilities.html')

@app.route('/calculate-weight', methods=['POST'])
def calculate_weight():
    try:
        earth_weight = float(request.form['weight'])
        planet = request.form['planet']
        gravity_factors = {
            'Mercury': 0.38,
            'Venus': 0.91,
            'Earth': 1,
            'Moon': 0.16,
            'Mars': 0.38,
            'Jupiter': 2.34,
            'Saturn': 1.06,
            'Uranus': 0.92,
            'Neptune': 1.19,
            'Pluto': 0.06
        }
        result = earth_weight * gravity_factors.get(planet, 1)
        return render_template('utilities.html', result=result, planet=planet)
    except:
        return render_template('utilities.html', error="Invalid input.")

@app.route('/iss-pass')
def iss_pass():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return {'error': 'Missing lat or lon'}, 400
    try:
        url = f'http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lon}'
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return {'error': 'Could not fetch ISS pass data'}, 500

if __name__ == '__main__':
    app.run(debug=True)
