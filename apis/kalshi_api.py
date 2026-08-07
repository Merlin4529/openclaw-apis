import requests
import os
from dotenv import load_dotenv

load_dotenv()

class KalshiAPI:
    def __init__(self):
        self.api_key = os.getenv('KALSHI_API_KEY', '')
        self.base_url = os.getenv('KALSHI_BASE_URL', 'https://demo-api.kalshi.co/trade-api/v2')
        self.timeout = 10
        self.headers = {'Content-Type': 'application/json'}
    
    def test_connection(self):
        """Test API connection"""
        url = f"{self.base_url}/exchange/status"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return response.status_code in [200, 401]  # 401 sin auth es normal
        except:
            return False
    
    def get_markets(self, ticker_filter=None):
        """Get all markets (can filter by ticker)"""
        url = f"{self.base_url}/markets"
        params = {}
        if ticker_filter:
            params['ticker_filter'] = ticker_filter
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_market(self, ticker):
        """Get specific market by ticker"""
        url = f"{self.base_url}/markets/{ticker}"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

if __name__ == "__main__":
    api = KalshiAPI()
    print(f"Connection: {api.test_connection()}")
