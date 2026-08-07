import requests
from config.api_keys import APICredentials
from cache.cache_manager import CacheManager

class FootyStatsAPI:
    def __init__(self):
        self.api_key = APICredentials.get_footystats_key()
        self.base_url = os.getenv('FOOTYSTATS_BASE_URL')
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
        self.cache = CacheManager()
