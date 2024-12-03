import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import random

load_dotenv()

class QuerySuggestionEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
        # Store previous suggestions to avoid repetition
        self.previous_suggestions = set()

    def get_random_query(self) -> str:
        """Generate a random YouTube search query idea"""
        topics = [
            "educational content",
            "technology tutorials",
            "creative projects",
            "science experiments",
            "historical events",
            "life hacks",
            "cultural experiences",
            "nature documentaries",
            "skill development",
            "innovative ideas"
        ]
        
        prompt = f"""Generate a unique and interesting YouTube search query about {random.choice(topics)}. 
        Make it specific, engaging, and different from common searches.
        It should be educational, entertaining, or inspiring.
        Return only the query text, nothing else.
        Avoid generic terms and make it creative."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a creative assistant that generates unique and specific YouTube search queries. Avoid generic suggestions and focus on interesting, specific topics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.9,  # Increased for more randomness
                presence_penalty=0.6,  # Added to encourage unique content
                frequency_penalty=0.6  # Added to discourage repetition
            )
            suggestion = response.choices[0].message.content.strip()
            
            # If we get a repeated suggestion, try again (up to 3 times)
            attempts = 0
            while suggestion in self.previous_suggestions and attempts < 3:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Generate a different, unique query."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    presence_penalty=0.8,
                    frequency_penalty=0.8
                )
                suggestion = response.choices[0].message.content.strip()
                attempts += 1
            
            self.previous_suggestions.add(suggestion)
            # Keep set size manageable
            if len(self.previous_suggestions) > 100:
                self.previous_suggestions.clear()
                
            return suggestion
        except Exception as e:
            return f"Error generating suggestion: {str(e)}"

    def get_related_queries(self, user_query: str, num_suggestions: int = 3) -> List[str]:
        """Generate related YouTube search query ideas based on user input"""
        prompt = f"""Based on the YouTube search query "{user_query}", 
        suggest {num_suggestions} unique and creative related search queries.
        Each suggestion should:
        1. Be different from the original query
        2. Explore a different aspect or perspective
        3. Be specific and interesting
        Return only the queries, one per line, without quotes or punctuation."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a creative assistant that generates diverse and unique YouTube search queries. Each suggestion should be distinctly different from others."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.9,
                presence_penalty=0.7,
                frequency_penalty=0.7
            )
            
            # Clean up and validate suggestions
            suggestions = response.choices[0].message.content.strip().split('\n')
            clean_suggestions = []
            
            for s in suggestions:
                cleaned = s.strip().strip('"\'').strip()
                # Only add if it's unique and not empty
                if cleaned and cleaned not in clean_suggestions:
                    clean_suggestions.append(cleaned)
            
            # If we don't have enough unique suggestions, try to get more
            if len(clean_suggestions) < num_suggestions:
                additional_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Generate more unique suggestions, different from previous ones."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.0,
                    presence_penalty=0.9,
                    frequency_penalty=0.9
                )
                
                additional_suggestions = additional_response.choices[0].message.content.strip().split('\n')
                for s in additional_suggestions:
                    cleaned = s.strip().strip('"\'').strip()
                    if cleaned and cleaned not in clean_suggestions:
                        clean_suggestions.append(cleaned)
            
            return clean_suggestions[:num_suggestions]
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"] 