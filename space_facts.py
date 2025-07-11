from groq import Groq
import random


class SpaceFactsGenerator:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.client = Groq(api_key=groq_api_key)
        self.fallback_facts = [
            "A day on Venus is longer than its year.",
            "There are more trees on Earth than stars in the Milky Way.",
            "The Moon is moving away from Earth by 3.8 cm every year.",
            "Neutron stars can spin at a rate of 600 rotations per second.",
            "One million Earths can fit inside the Sun.",
            "Jupiter's Great Red Spot is a storm larger than Earth.",
            "Saturn's rings are made mostly of ice and rock.",
            "Light from the Sun takes about 8 minutes to reach Earth.",
            "The Milky Way galaxy contains over 100 billion stars.",
            "Space is completely silent due to lack of atmosphere.",
        ]

    def generate_facts(self, count=5):
        """Generate space facts using Groq API"""
        try:
            system_prompt = f"""You are a space facts generator. Generate exactly {count} fascinating, accurate, and mind-blowing space facts. Each fact should be:
            - Scientifically accurate and verifiable
            - Concise (under 50 characters)
            - Amazing and thought-provoking
            - About different aspects of space (planets, stars, galaxies, phenomena, etc.)
            - Suitable for general audiences
            
            Format your response as a simple list with each fact on a new line, starting with a dash (-).
            Do not include any introductory text, explanations, or additional commentary."""

            user_prompt = f"Generate {count} new fascinating space facts that are different from commonly known ones."

            chat_completion = self.client.chat.completions.create(
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

            # Ensure we have exactly the requested number of facts
            if len(fun_facts) < count:
                # Add fallback facts if needed
                needed_facts = count - len(fun_facts)
                available_fallbacks = random.sample(
                    self.fallback_facts, min(needed_facts, len(self.fallback_facts))
                )
                fun_facts.extend(available_fallbacks)
            elif len(fun_facts) > count:
                fun_facts = fun_facts[:count]

            return fun_facts

        except Exception as e:
            print(f"Error generating facts with Groq: {e}")
            # Return random fallback facts if API fails
            return random.sample(
                self.fallback_facts, min(count, len(self.fallback_facts))
            )

    def get_random_fact(self, facts=None):
        """Get a single random fact"""
        if facts is None:
            facts = self.generate_facts(5)
        return random.choice(facts)
