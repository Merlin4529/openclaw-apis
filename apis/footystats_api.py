import requests
import os
from dotenv import load_dotenv

load_dotenv()

class FootyStatsAPI:
    def __init__(self):
        self.api_key = os.getenv('FOOTYSTATS_API_KEY')
        self.base_url = os.getenv('FOOTYSTATS_BASE_URL', 'https://api.football-data-api.com')
        self.timeout = 10
    
    def test_connection(self):
        """Test API connection"""
        url = f"{self.base_url}/test-call?key={self.api_key}"
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.status_code == 200
        except:
            return False
    
    def get_league_matches(self, season_id, page=1, max_per_page=500):
        """Get all matches for a league"""
        url = f"{self.base_url}/league-matches"
        params = {
            'key': self.api_key,
            'season_id': season_id,
            'page': page,
            'max_per_page': max_per_page
        }
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

if __name__ == "__main__":
    api = FootyStatsAPI()
    print(f"Connection: {api.test_connection()}")
