import os
from dotenv import load_dotenv

load_dotenv()

class APICredentials:
    @staticmethod
    def get_footystats_key():
        return os.getenv('FOOTYSTATS_API_KEY')
    
    @staticmethod
    def get_cache_ttl():
        return int(os.getenv('CACHE_TTL', 300))
