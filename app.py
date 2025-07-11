from flask import Flask, render_template
import requests

app = Flask(__name__)

NASA_API_KEY = "8gldDFCSaaAFEEsld1qYR2BAqCywsEmDCH1gkb3m"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/asteroids')
def asteroids():
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-07-11&api_key={NASA_API_KEY}"
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

@app.route('/news')
def news():
    news_url = "https://api.spaceflightnewsapi.net/v4/articles"
    res = requests.get(news_url)
    articles = res.json()['results'][:10]  # Latest 10 articles
    return render_template('news.html', articles=articles)

@app.route('/events')
def events():
    event_url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=5"
    res = requests.get(event_url)
    events = res.json()['results']
    return render_template('events.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)
