"""
GAMBLER AGENT v3.0
Lee predicciones de HARPO + cuotas de Kalshi
Calcula Expected Value (EV)
Decide si apostar automáticamente
Output: Órdenes para Kalshi
"""

import json
from datetime import datetime

class GamblerAgentV3:
    def __init__(self, bankroll=1000, kelly_fraction=0.05, min_ev=0.05):
        self.bankroll = bankroll
        self.kelly_fraction = kelly_fraction  # Criterio Kelly fraccionado
        self.min_ev = min_ev  # EV mínimo requerido (5%)
        self.pending_orders = []
    
    def calculate_ev(self, probability, odds):
        """Calcular Expected Value"""
        if odds <= 0:
            return -1
        return (probability * odds) - 1
    
    def calculate_bet_size(self, probability, odds):
        """Calcular tamaño de apuesta con Criterio Kelly"""
        ev = self.calculate_ev(probability, odds)
        if ev <= self.min_ev:
            return 0
        
        kelly = (probability * odds - 1) / (odds - 1)
        fractional_kelly = kelly * self.kelly_fraction
        
        if fractional_kelly < 0.01:
            return 0
        
        bet_size = self.bankroll * fractional_kelly
        return min(bet_size, self.bankroll * 0.1)  # Max 10% del bankroll
    
    def evaluate_prediction(self, prediction, odds_dict):
        """Evaluar si apostar en una predicción"""
        outcome = prediction['predictions']['predicted_outcome']
        confidence = prediction['predictions']['confidence']
        
        odds = odds_dict.get(outcome, 0)
        if odds <= 1:
            return None
        
        ev = self.calculate_ev(confidence, odds)
        bet_size = self.calculate_bet_size(confidence, odds)
        
        if bet_size == 0:
            return None
        
        return {
            'match_id': prediction['match_id'],
            'outcome': outcome,
            'probability': confidence,
            'odds': odds,
            'ev': ev,
            'bet_size': bet_size,
            'expected_return': bet_size * odds,
            'status': 'ready_to_place'
        }
    
    def process(self, harpo_output):
        """Procesar predicciones y generar órdenes"""
        print("\n" + "="*60)
        print("[GAMBLER AGENT v3.0] INICIANDO")
        print("="*60)
        
        predictions = harpo_output.get('predictions', [])
        orders = []
        total_risk = 0
        total_potential_return = 0
        
        for pred in predictions:
            odds = pred.get('odds', {})
            order = self.evaluate_prediction(pred, odds)
            
            if order:
                orders.append(order)
                total_risk += order['bet_size']
                total_potential_return += order['expected_return']
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_orders': len(orders),
            'total_risk': total_risk,
            'total_potential_return': total_potential_return,
            'bankroll': self.bankroll,
            'orders': orders
        }
        
        print(f"[GAMBLER] {len(orders)} órdenes generadas")
        print(f"[GAMBLER] Riesgo total: ${total_risk:.2f}")
        print(f"[GAMBLER] Retorno potencial: ${total_potential_return:.2f}")
        print("[GAMBLER AGENT v3.0] COMPLETADO\n")
        
        return output

if __name__ == "__main__":
    # Test con datos dummy
    test_harpo_output = {
        'predictions': [
            {
                'match_id': 1,
                'predictions': {'predicted_outcome': 'home', 'confidence': 0.689},
                'odds': {'home': 1.5, 'draw': 3.2, 'away': 6.0}
            }
        ]
    }
    agent = GamblerAgentV3()
    result = agent.process(test_harpo_output)
    print(json.dumps(result, indent=2))
