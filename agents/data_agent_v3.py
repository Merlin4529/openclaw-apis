"""
DATA AGENT v3.0
Combina FootyStats (datos de partidos) + Kalshi (cuotas)
Output: JSON normalizado con todos los datos necesarios
"""

import json
import sys
sys.path.insert(0, '.')
from datetime import datetime
from apis.footystats_api import FootyStatsAPI
from apis.kalshi_api import KalshiAPI

class DataAgentV3:
    def __init__(self):
        self.footystats = FootyStatsAPI()
        self.kalshi = KalshiAPI()
        self.argentina_season_id = 5582
    
    def get_league_matches(self):
        print("[DATA] Obteniendo partidos...")
        data = self.footystats.get_league_matches(self.argentina_season_id)
        if data and data.get('success'):
            return data.get('data', [])
        return []
    
    def normalize_match_data(self, match):
        return {
            'match_id': match.get('id'),
            'home_team_id': match.get('homeID'),
            'away_team_id': match.get('awayID'),
            'status': match.get('status'),
            'game_week': match.get('game_week'),
            'home_goals': match.get('homeGoalCount'),
            'away_goals': match.get('awayGoalCount'),
            'odds': {
                '1X2': {'home': match.get('odds_ft_1'), 'draw': match.get('odds_ft_x'), 'away': match.get('odds_ft_2')},
                'over_under': {'over_25': match.get('odds_ft_over25'), 'under_25': match.get('odds_ft_under25')}
            }
        }
    
    def process(self):
        print("\n" + "="*60)
        print("[DATA AGENT v3.0] INICIANDO")
        print("="*60)
        
        matches = self.get_league_matches()
        normalized = [self.normalize_match_data(m) for m in matches]
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'league': 'Liga Argentina',
            'total_matches': len(normalized),
            'matches': normalized
        }
        
        print(f"[DATA] {len(normalized)} partidos procesados")
        print("[DATA AGENT v3.0] COMPLETADO\n")
        return output

if __name__ == "__main__":
    agent = DataAgentV3()
    result = agent.process()
    print(json.dumps(result, indent=2)[:300])
