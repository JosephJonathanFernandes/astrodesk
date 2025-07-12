from flask import Flask, render_template, request, jsonify, Response
import requests
import random
from groq import Groq
import json
from workflow import AstroBotWorkflow
from space_facts import SpaceFactsGenerator
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import datetime, timedelta
from skyfield.api import utc
from story import SpaceTravelStoryGenerator


app = Flask(__name__)

NASA_API_KEY = "8gldDFCSaaAFEEsld1qYR2BAqCywsEmDCH1gkb3m"
GROQ_API_KEY = "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"
astro_workflow = AstroBotWorkflow(GROQ_API_KEY)
space_facts_generator = SpaceFactsGenerator(GROQ_API_KEY)
story_generator = SpaceTravelStoryGenerator(GROQ_API_KEY)


eph = load("de421.bsp")
ts = load.timescale()


@app.route("/")
def home():
    fun_facts = space_facts_generator.generate_facts(count=5)
    random_fact = space_facts_generator.get_random_fact(fun_facts)
    return render_template("index.html", fun_facts=fun_facts, random_fact=random_fact)


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        session_id = data.get("session_id", "default")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        def generate():
            try:
                response_content = astro_workflow.invoke_streaming(
                    user_message, session_id
                )
                for char in response_content:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(generate(), mimetype="text/event-stream")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat/status", methods=["GET"])
def chat_status():
    try:
        session_id = request.args.get("session_id", "default")
        status = astro_workflow.get_conversation_state(session_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/asteroids")
def asteroids():
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-07-11&api_key={NASA_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        asteroid_list = []
        for date in data["near_earth_objects"]:
            for asteroid in data["near_earth_objects"][date]:
                asteroid_list.append(
                    {
                        "name": asteroid["name"],
                        "close_approach": asteroid["close_approach_data"][0][
                            "close_approach_date"
                        ],
                        "velocity": asteroid["close_approach_data"][0][
                            "relative_velocity"
                        ]["kilometers_per_hour"],
                        "distance": asteroid["close_approach_data"][0]["miss_distance"][
                            "kilometers"
                        ],
                    }
                )
        return render_template("asteroids.html", asteroids=asteroid_list)
    except Exception as e:
        return render_template(
            "error.html", message="Asteroid data not available right now."
        )


@app.route("/news")
def news():
    news_url = "https://api.spaceflightnewsapi.net/v4/articles"
    try:
        res = requests.get(news_url)
        articles = res.json()["results"][:10]
        return render_template("news.html", articles=articles)
    except:
        return render_template(
            "error.html", message="Space news is currently unavailable."
        )


@app.route("/events")
def events():
    event_url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=5"
    try:
        res = requests.get(event_url)
        events = res.json()["results"]
        return render_template("events.html", events=events)
    except:
        return render_template(
            "error.html", message="Space events could not be fetched."
        )


@app.route("/utilities")
def utilities():
    return render_template("utilities.html")


@app.route("/calculate-weight", methods=["POST"])
def calculate_weight():
    try:
        earth_weight = float(request.form["weight"])
        planet = request.form["planet"]
        gravity_factors = {
            "Mercury": 0.38,
            "Venus": 0.91,
            "Earth": 1,
            "Moon": 0.16,
            "Mars": 0.38,
            "Jupiter": 2.34,
            "Saturn": 1.06,
            "Uranus": 0.92,
            "Neptune": 1.19,
            "Pluto": 0.06,
        }
        result = earth_weight * gravity_factors.get(planet, 1)
        return render_template("utilities.html", result=result, planet=planet)
    except:
        return render_template("utilities.html", error="Invalid input.")


@app.route("/story", methods=["GET", "POST"])
def story():
    if request.method == "POST":
        destination = request.form.get("destination")
        if destination:
            # Generate the story
            story_result = story_generator.generate_travel_story(destination)
            return render_template("story.html", story_result=story_result)

    # GET request - show the form
    return render_template("story.html")


@app.route("/iss-pass")
def iss_pass():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return {"error": "Missing lat or lon"}, 400
    try:
        url = f"http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lon}"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return {"error": "Could not fetch ISS pass data"}, 500


@app.route("/stargazer-guide", methods=["POST"])
def stargazer_guide():
    location = request.form["location"]
    city_coords = {
        "Goa": ("15.2993 N", "74.1240 E"),
        "Delhi": ("28.7041 N", "77.1025 E"),
        "Bangalore": ("12.9716 N", "77.5946 E"),
        "Mumbai": ("19.0760 N", "72.8777 E"),
        "Chennai": ("13.0827 N", "80.2707 E"),
    }
    lat, lon = city_coords.get(location, ("15.2993 N", "74.1240 E"))
    topos = Topos(lat, lon)
    t_now = ts.utc(datetime.utcnow().replace(tzinfo=utc))
    moon_phase_angle = almanac.moon_phase(eph, t_now).degrees
    f = almanac.sunrise_sunset(eph, topos)
    t0 = t_now
    t1 = ts.utc((datetime.utcnow() + timedelta(days=1)).replace(tzinfo=utc))
    times, events = almanac.find_discrete(t0, t1, f)
    sunrise_time = "Not found"
    sunset_time = "Not found"
    for ti, event in zip(times, events):
        if event == 1 and sunrise_time == "Not found":
            sunrise_time = ti.utc_strftime("%Y-%m-%d %H:%M:%S")
        if event == 0 and sunset_time == "Not found":
            sunset_time = ti.utc_strftime("%Y-%m-%d %H:%M:%S")
    visible_objects = [
        {
            "object": "Moon Phase Angle",
            "direction": "Sky",
            "time": f"{moon_phase_angle:.1f}°",
        },
        {"object": "Sunrise", "direction": "East", "time": sunrise_time},
        {"object": "Sunset", "direction": "West", "time": sunset_time},
    ]
    return render_template(
        "stargazer.html", location=location, visible_objects=visible_objects
    )


@app.route("/planet-positions")
def planet_positions():
    t_now = ts.utc(datetime.utcnow().replace(tzinfo=utc))
    planets = ["mercury", "venus", "mars", "jupiter barycenter", "saturn barycenter"]
    positions = {}
    for name in planets:
        planet = eph[name]
        astrometric = planet.at(t_now).ecliptic_position().au
        positions[name.title()] = {
            "x": float(astrometric[0]),
            "y": float(astrometric[1]),
            "z": float(astrometric[2]),
        }
    return jsonify(positions)


@app.route("/moon-phase-by-date", methods=["POST"])
def moon_phase_by_date():
    date_str = request.form["date"]
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=utc)
        t = ts.utc(date_obj)
        phase_angle = almanac.moon_phase(eph, t).degrees
        return jsonify({"date": date_str, "moon_phase_angle": f"{phase_angle:.1f}°"})
    except:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."})


@app.route("/stargazer")
def stargazer():
    return render_template("stargazer.html")


@app.route("/planet-positions-graph")
def planet_positions_graph():
    return render_template("planet_positions_graph.html")


if __name__ == "__main__":
    app.run(debug=True)
