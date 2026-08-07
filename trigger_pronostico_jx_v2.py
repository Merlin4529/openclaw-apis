import json, sys
sys.path.insert(0, '.')
from agents.data_agent_v3 import DataAgentV3
from agents.harpo_agent_v3 import HarpoAgentV3
from agents.gambler_agent_v3 import GamblerAgentV3
from agents.tango_agent_v3 import TangoAgentV3
from agents.news_agent_v3 import NewsAgentV3

def run_pipeline():
    print("\n" + "="*70)
    print("OPENCLAW v3.0 - 6 AGENTS (DATA->HARPO->NEWS->GAMBLER->TANGO)")
    print("="*70)
    
    data_agent = DataAgentV3()
    data_output = data_agent.process()
    
    harpo_agent = HarpoAgentV3()
    harpo_output = harpo_agent.process(data_output)
    
    news_agent = NewsAgentV3()
    news_output = news_agent.process_predictions(harpo_output, [])
    
    gambler_agent = GamblerAgentV3()
    gambler_output = gambler_agent.process(news_output)
    
    tango_agent = TangoAgentV3()
    tango_output = tango_agent.audit(news_output, [])
    
    print("\n[6/6] REPORTE FINAL")
    final_report = {
        'status': 'success',
        'pipeline': 'DATA -> HARPO -> NEWS -> GAMBLER -> TANGO',
        'agents': {
            'data': data_output.get('total_matches'),
            'harpo': harpo_output.get('total_predictions'),
            'news': 'analyzed',
            'gambler': gambler_output.get('total_orders'),
            'tango': tango_output.get('accuracy')
        }
    }
    
    print("\n" + "="*70)
    print("REPORTE FINAL - 6 AGENTS")
    print("="*70)
    print(json.dumps(final_report, indent=2))
    return final_report

if __name__ == "__main__":
    run_pipeline()
