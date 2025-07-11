from flask import Flask, render_template, request, jsonify, Response
import requests
import random
from groq import Groq
import json

app = Flask(__name__)

NASA_API_KEY = "8gldDFCSaaAFEEsld1qYR2BAqCywsEmDCH1gkb3m"
GROQ_API_KEY = "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"  # Replace with your actual GROQ API key


@app.route("/")
def home():
    client = Groq(api_key=GROQ_API_KEY)

    # Fallback facts in case API fails
    fallback_facts = [
        "A day on Venus is longer than its year.",
        "There are more trees on Earth than stars in the Milky Way.",
        "The Moon is moving away from Earth by 3.8 cm every year.",
        "Neutron stars can spin at a rate of 600 rotations per second.",
        "One million Earths can fit inside the Sun.",
    ]

    try:
        # System prompt for generating space facts
        system_prompt = """You are a space facts generator. Generate exactly 5 fascinating, accurate, and mind-blowing space facts. Each fact should be:
        - Scientifically accurate and verifiable
        - Concise (under 50 characters)
        - Amazing and thought-provoking
        - About different aspects of space (planets, stars, galaxies, phenomena, etc.)
        - Suitable for general audiences
        - rather than showing numbers, use descriptive phrases
        
        Format your response as a simple list with each fact on a new line, starting with a dash (-).
        Do not include any introductory text, explanations, or additional commentary.
        
        Example format:
        - Fact 1 here
        - Fact 2 here
        - Fact 3 here
        - Fact 4 here
        - Fact 5 here"""

        user_prompt = "Generate 5 new fascinating space facts that are different from commonly known ones."

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama3-8b-8192",
            temperature=0.8,
            max_tokens=400,
            stream=False,
        )

        # Parse the response to extract facts
        response_text = chat_completion.choices[0].message.content.strip()

        # Extract facts from the response
        fun_facts = []
        lines = response_text.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("-"):
                fact = line[1:].strip()
                if fact:
                    fun_facts.append(fact)

        # Ensure we have exactly 5 facts
        if len(fun_facts) < 5:
            # Add fallback facts if needed
            fun_facts.extend(fallback_facts[: 5 - len(fun_facts)])
        elif len(fun_facts) > 5:
            fun_facts = fun_facts[:5]

    except Exception as e:
        print(f"Error generating facts with Groq: {e}")
        # Use fallback facts if API fails
        fun_facts = fallback_facts

    # Select a random fact from the generated/fallback facts
    random_fact = random.choice(fun_facts)

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

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        client = Groq(api_key=GROQ_API_KEY)

        # Create a space-themed system prompt
        system_prompt = """You are AstroBot, a friendly and knowledgeable space assistant. You help users learn about astronomy, space exploration, planets, stars, galaxies, and all things related to space science. 
        
        Key guidelines:
        - Keep responses informative yet engaging
        - Use space-related emojis occasionally (🚀, 🌌, ⭐, 🪐, 🌙, 🛰️)
        - Explain complex concepts in simple terms
        - If asked about something not space-related, gently redirect to space topics
        - Keep responses concise but thorough, aiming for 2-3 sentences
        
        - Include fascinating space facts when relevant"""

        def generate():
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    model="llama3-8b-8192",
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True,
                )

                for chunk in chat_completion:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'content': content})}\n\n"

                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(generate(), mimetype="text/event-stream")

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
