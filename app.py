from flask import Flask, render_template, request, jsonify, Response
import requests
import random
from groq import Groq
import json
from workflow import AstroBotWorkflow
from space_facts import SpaceFactsGenerator

app = Flask(__name__)

NASA_API_KEY = "8gldDFCSaaAFEEsld1qYR2BAqCywsEmDCH1gkb3m"
GROQ_API_KEY = "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"  # Replace with your actual GROQ API key
astro_workflow = AstroBotWorkflow(GROQ_API_KEY)
space_facts_generator = SpaceFactsGenerator(GROQ_API_KEY)


@app.route("/")
def home():
    # Generate space facts using the SpaceFactsGenerator
    fun_facts = space_facts_generator.generate_facts(count=5)

    # Select a random fact from the generated facts
    random_fact = space_facts_generator.get_random_fact(fun_facts)

    return render_template("index.html", fun_facts=fun_facts, random_fact=random_fact)


# Add this route to your app.py
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
                # Get response from workflow
                response_content = astro_workflow.invoke_streaming(
                    user_message, session_id
                )

                # Stream the response character by character for better UX
                for char in response_content:
                    yield f"data: {json.dumps({'content': char})}\n\n"

                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(generate(), mimetype="text/event-stream")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add this route to get conversation status
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


if __name__ == "__main__":
    app.run(debug=True)
