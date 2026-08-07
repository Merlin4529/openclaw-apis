"""
HARPO AGENT v3.0
Lee datos normalizados del DATA AGENT
Aplica modelo de predicción (Elo + xG)
Output: Predicciones con probabilidades y confianza
"""

import json
from datetime import datetime

class HarpoAgentV3:
    def __init__(self):
        # Elo ratings base Liga Argentina (actualizar según resultados)
        self.elo_ratings = {
            1700: 1700,  # River Plate
            1680: 1680,  # Boca Juniors
            1670: 1670,  # Racing Club
            1650: 1650,  # Independiente
            1640: 1640,  # San Lorenzo
            1630: 1630,  # Vélez Sarsfield
            1620: 1620,  # Estudiantes
            1610: 1610,  # Defensa y Justicia
        }
        self.home_advantage = 1.15
        self.base_confidence = 0.71
    
    def calculate_probability(self, home_elo, away_elo):
        """Calcular probabilidad usando formula Elo"""
        diff = home_elo - away_elo
        home_prob = 1 / (1 + 10 ** (-diff / 400))
        draw_prob = 0.25
        away_prob = 1 - home_prob - draw_prob
        return {
            'home': min(0.90, home_prob * self.home_advantage),
            'draw': draw_prob,
            'away': max(0.05, away_prob)
        }
    
    def predict_match(self, match_data):
        """Predecir un partido individual"""
        home_id = match_data.get('home_team_id', 1700)
        away_id = match_data.get('away_team_id', 1630)
        
        home_elo = self.elo_ratings.get(home_id, 1650)
        away_elo = self.elo_ratings.get(away_id, 1650)
        
        probs = self.calculate_probability(home_elo, away_elo)
        
        # Extraer cuotas
        odds_1x2 = match_data.get('odds', {}).get('1X2', {})
        
        return {
            'match_id': match_data.get('match_id'),
            'home_team_id': home_id,
            'away_team_id': away_id,
            'home_elo': home_elo,
            'away_elo': away_elo,
            'predictions': {
                'probabilities': probs,
                'predicted_outcome': max(probs, key=probs.get),
                'confidence': max(probs.values())
            },
            'odds': odds_1x2
        }
    
    def process(self, data_agent_output):
        """Procesar predicciones para todos los partidos"""
        print("\n" + "="*60)
        print("[HARPO AGENT v3.0] INICIANDO")
        print("="*60)
        
        matches = data_agent_output.get('matches', [])
        predictions = [self.predict_match(m) for m in matches]
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_predictions': len(predictions),
            'average_confidence': sum(p['predictions']['confidence'] for p in predictions) / max(1, len(predictions)),
            'predictions': predictions
        }
        
        print(f"[HARPO] {len(predictions)} predicciones generadas")
        print(f"[HARPO] Confianza promedio: {output['average_confidence']:.2%}")
        print("[HARPO AGENT v3.0] COMPLETADO\n")
        
        return output

if __name__ == "__main__":
    # Test con datos dummy
    test_data = {
        'matches': [
            {'match_id': 1, 'home_team_id': 1700, 'away_team_id': 1630, 'odds': {'1X2': {'home': 1.5, 'draw': 3.2, 'away': 6.0}}}
        ]
    }
    agent = HarpoAgentV3()
    result = agent.process(test_data)
    print(json.dumps(result, indent=2))
