import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class QuerySuggestionEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

    def get_random_query(self) -> str:
        """Generate a random YouTube search query idea"""
        prompt = """Generate a random, interesting YouTube search query. 
        It should be something educational, entertaining, or inspiring. 
        Return only the query text, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates YouTube search queries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating suggestion: {str(e)}"

    def get_related_queries(self, user_query: str, num_suggestions: int = 4) -> List[str]:
        """Generate related YouTube search query ideas based on user input"""
        prompt = f"""Based on the YouTube search query "{user_query}", 
        suggest {num_suggestions} related but different search queries.
        Return only the queries, one per line, without quotes or extra punctuation."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates related YouTube search queries. Return only plain text queries without quotes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            # Clean up suggestions by removing quotes and extra whitespace
            suggestions = response.choices[0].message.content.strip().split('\n')
            return [s.strip().strip('"\'').strip() for s in suggestions if s.strip()]
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"] 