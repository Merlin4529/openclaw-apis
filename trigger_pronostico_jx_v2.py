import json, sys
sys.path.insert(0, '.')
from agents.data_agent_v3 import DataAgentV3
from agents.harpo_agent_v3 import HarpoAgentV3
from agents.gambler_agent_v3 import GamblerAgentV3
from agents.tango_agent_v3 import TangoAgentV3

def run_pipeline():
    print("\n" + "="*70)
    print("OPENCLAW PRONOSTICOS v2.0 - PIPELINE COMPLETO (5 AGENTS)")
    print("="*70)
    
    data_agent = DataAgentV3()
    data_output = data_agent.process()
    
    harpo_agent = HarpoAgentV3()
    harpo_output = harpo_agent.process(data_output)
    
    gambler_agent = GamblerAgentV3()
    gambler_output = gambler_agent.process(harpo_output)
    
    tango_agent = TangoAgentV3()
    tango_output = tango_agent.audit(harpo_output, [])
    
    print("\n[5/5] REPORTE FINAL")
    final_report = {
        'status': 'success',
        'pipeline': 'DATA -> HARPO -> GAMBLER -> TANGO',
        'data_stage': {'total_matches': data_output.get('total_matches')},
        'harpo_stage': {'predictions': harpo_output.get('total_predictions')},
        'gambler_stage': {'orders': gambler_output.get('total_orders')},
        'tango_stage': {'accuracy': tango_output.get('accuracy')}
    }
    
    print("\n" + "="*70)
    print("REPORTE FINAL")
    print("="*70)
    print(json.dumps(final_report, indent=2))
    
    return final_report

if __name__ == "__main__":
    run_pipeline()
