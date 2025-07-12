from groq import Groq
import random


class SpaceTravelStoryGenerator:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.client = Groq(api_key=groq_api_key)

        # Available destinations
        self.destinations = [
            "Mars",
            "Jupiter",
            "Saturn",
            "Sun",
            "Black Hole",
            "Moon",
            "Venus",
            "Neptune",
            "Europa",
            "Titan",
            "Alpha Centauri",
            "Asteroid Belt",
            "Mercury",
            "Uranus",
            "Pluto",
        ]

        # Available moods for story generation
        self.moods = [
            "sarcastic",
            "scary",
            "adventurous",
            "wonder",
            "awe inspiring",
            "humorous",
            "mysterious",
            "thrilling",
            "contemplative",
            "playful",
            "Suspenseful",
            "Bored and lazy",
            "depressed",
            "Indian Mass Masala",
        ]

    def get_available_destinations(self):
        """Get list of all available destinations"""
        return self.destinations

    def _get_location_features(self, destination):
        """Agent 1: Analyze destination features"""
        try:
            system_prompt = """You are a space research analyst. Analyze the given celestial destination and provide exactly 4 amazing positive features and 4 negative/dangerous features. Be factual and scientific.

            FORMAT YOUR RESPONSE EXACTLY AS:
            POSITIVE FEATURES:
            • [feature 1]
            • [feature 2]
            • [feature 3]
            • [feature 4]

            NEGATIVE FEATURES:
            • [feature 1]
            • [feature 2]
            • [feature 3]
            • [feature 4]

            Keep each point concise and factual."""

            user_prompt = f"Analyze {destination} and provide 4 positive features and 4 negative/dangerous features for space travel."

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama3-70b-8192",
                temperature=0.3,
                max_tokens=300,
                stream=False,
            )

            features_text = chat_completion.choices[0].message.content.strip()
            return {"success": True, "features": features_text}

        except Exception as e:
            print(f"Error getting location features: {e}")
            return {
                "success": False,
                "features": f"POSITIVE FEATURES:\n• Beautiful cosmic views\n• Unique scientific phenomena\n• Inspiring celestial environment\n• Educational experience\n\nNEGATIVE FEATURES:\n• Extreme temperatures\n• Radiation exposure\n• Equipment challenges\n• Communication delays",
            }

    def _get_story_structure(self, destination, features, selected_moods):
        """Agent 2: Create story structure and word distribution"""
        try:
            system_prompt = """You are a story structure specialist. Create a flexible, mood-driven story structure for a space travel adventure. The story must be EXACTLY 250 words total.

            REQUIREMENTS:
            - Distribute words across 4 paragraphs based on selected moods
            - Create dynamic structure that emphasizes different story elements based on mood
            - Incorporate the given features and moods strategically
            - Provide specific instructions for the writer
            - Story must be first-person, entertaining, and engaging

            MOOD-BASED STRUCTURE GUIDELINES:
            - WONDER/AWE INSPIRING: Focus on journey descriptions and cosmic beauty
            - THRILLING/ADVENTUROUS: Emphasize action and challenges
            - SCARY/MYSTERIOUS: Build tension and unknown elements
            - HUMOROUS/SARCASTIC: Include witty observations and funny situations
            - CONTEMPLATIVE: Focus on philosophical reflections and realizations
            - PLAYFUL: Include lighthearted moments and creative scenarios

            FORMAT YOUR RESPONSE AS:
            STORY STRUCTURE (250 words total):

            PARAGRAPH 1 - [CUSTOM FOCUS based on mood] (word count):
            [Specific instructions for writer including mood and features to include]

            PARAGRAPH 2 - [CUSTOM FOCUS based on mood] (word count):
            [Specific instructions for writer including mood and features to include]

            PARAGRAPH 3 - [CUSTOM FOCUS based on mood] (word count):
            [Specific instructions for writer including mood and features to include]

            PARAGRAPH 4 - [CUSTOM FOCUS based on mood] (word count):
            [Specific instructions for writer including mood and features to include]
            
            One example of structure is:
            paragraph 1: launch and journey(50)
            paragraph 2: arrival and exploration(100)
            paragraph 3: challenges and discoveries(75)
            paragraph 4: conclusion and reflections(25)
            
            this is an example only, yours will differ based on mood and severity of location. 
            

            WRITING STYLE INSTRUCTIONS:
            [Specific style guidelines based on selected moods]

            Create a structure that best showcases the selected moods rather than following a fixed formula."""

            user_prompt = f"""Create a story structure for a space adventure to {destination}.

            DESTINATION FEATURES:
            {features}

            SELECTED MOODS: {', '.join(selected_moods)}

            Create paragraph-by-paragraph instructions for the writer, ensuring total word count is exactly 250 words."""

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama3-70b-8192",
                temperature=0.4,
                max_tokens=500,
                stream=False,
            )

            structure_text = chat_completion.choices[0].message.content.strip()
            return {"success": True, "structure": structure_text}

        except Exception as e:
            print(f"Error getting story structure: {e}")
            return {
                "success": False,
                "structure": f"STORY STRUCTURE: 4 paragraphs, 250 words total, {', '.join(selected_moods)} mood, incorporating features of {destination}",
            }

    def _write_story(self, destination, structure, selected_moods):
        """Agent 3: Write the actual story based on structure"""
        try:
            system_prompt = """You are a master storyteller. Write an engaging first-person space adventure story following the exact structure provided. 

            CRITICAL REQUIREMENTS:
            - Follow the structure EXACTLY as provided
            - Write EXACTLY 250 words total
            - Make it entertaining and engaging
            - Use first-person perspective
            - Include scientific elements naturally
            - NO AI prompts or meta-commentary
            - ONLY return the story text
            - NO phrases like "Here's the story" or "Here it is"
            - Blend in the styles of Chetan Bhagat and Ruskin bond 
            - make it relatable and write in a simple easy to understand language.
            - do not use too much poetic style, use the relatable and humourous side of Chetan Bhagat and only use the engaging ability of Ruskin Bond.
            

            Write the story directly without any introduction or conclusion remarks."""

            user_prompt = f"""Write a 250-word space adventure story to {destination} following this structure:

            {structure}

            MOODS TO INCORPORATE: {', '.join(selected_moods)}

            Write only the story - no additional text or commentary."""

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                max_tokens=400,
                stream=False,
            )

            story_text = chat_completion.choices[0].message.content.strip()

            # Clean up any unwanted AI prompts
            if story_text.lower().startswith(("here's", "here is", "here it is")):
                lines = story_text.split("\n")
                story_text = "\n".join(lines[1:]).strip()

            return {"success": True, "story": story_text}

        except Exception as e:
            print(f"Error writing story: {e}")
            return {"success": False, "story": self._get_fallback_story(destination)}

    def generate_travel_story(self, destination):
        """Main workflow combining all three agents"""
        try:
            # Step 1: Get location features
            print(f"Analyzing {destination} features...")
            features_result = self._get_location_features(destination)
            if not features_result["success"]:
                print("Using fallback features")

            # Step 2: Select random moods
            selected_moods = random.sample(self.moods, 2)
            print(f"Selected moods: {', '.join(selected_moods)}")

            # Step 3: Get story structure
            print("Creating story structure...")
            structure_result = self._get_story_structure(
                destination, features_result["features"], selected_moods
            )
            if not structure_result["success"]:
                print("Using fallback structure")

            # Step 4: Write the story
            print("Writing the story...")
            story_result = self._write_story(
                destination, structure_result["structure"], selected_moods
            )

            if story_result["success"]:
                return {
                    "success": True,
                    "story": story_result["story"],
                    "destination": destination,
                    "moods": selected_moods,
                    "features": features_result["features"],
                }
            else:
                return {
                    "success": False,
                    "error": "Story generation failed",
                    "story": self._get_fallback_story(destination),
                    "destination": destination,
                    "moods": selected_moods,
                }

        except Exception as e:
            print(f"Error in story generation workflow: {e}")
            return {
                "success": False,
                "error": str(e),
                "story": self._get_fallback_story(destination),
                "destination": destination,
                "moods": ["adventurous", "wonder"],
            }

    def _get_fallback_story(self, destination):
        """Enhanced fallback story with engaging style if AI fails"""
        return f"""So there I was, sitting in my spacecraft, thinking "Well, this is it" as Earth slowly became a tiny blue marble behind me. The journey to {destination} was like nothing I'd ever experienced - imagine watching the most beautiful documentary, except you're actually living it. My heart raced as we approached, and I couldn't help but grin like a kid on Christmas morning.

        When I finally reached {destination}, I just stood there for a moment, completely mesmerized. It was like seeing a masterpiece painting for the first time - every detail was perfect, every feature told a story. The scientific facts I'd memorized suddenly came alive, and I found myself genuinely moved by the beauty of it all. The colors, the textures, the sheer scale of everything left me speechless.

        Of course, that's when things got interesting. My equipment decided to have a tantrum, beeping and flashing like it was auditioning for a disco. I'll admit, I panicked for a second. Space has a funny way of reminding you that you're just a tiny human in a very big universe. But sometimes, the best adventures come from the most unexpected challenges.

        But you know what? Solving that problem taught me something profound. {destination} wasn't just a destination - it was a teacher, showing me that courage isn't the absence of fear, it's doing something amazing despite it."""

    def get_random_destination(self):
        """Get a random destination for surprise adventures"""
        return random.choice(self.destinations)
