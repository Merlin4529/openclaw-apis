"""
SCHEDULER - Ejecuta pipeline automáticamente
Liga Argentina: Viernes, Sábado, Domingo
Horarios: 10:00, 14:00, 18:00, 21:00 (ART)
"""

import schedule
import time
import json
from datetime import datetime
from trigger_pronostico_jx_v2 import run_pipeline

class SchedulerPronosticos:
    def __init__(self):
        self.log_file = 'logs/scheduler.log'
        self.ensure_logs_dir()
    
    def ensure_logs_dir(self):
        import os
        os.makedirs('logs', exist_ok=True)
    
    def log(self, message):
        """Guardar log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def job_pipeline(self):
        """Ejecutar pipeline y guardar resultado"""
        self.log("="*70)
        self.log("INICIANDO EJECUCION DEL PIPELINE")
        self.log("="*70)
        
        try:
            result = run_pipeline()
            
            # Guardar resultado en JSON
            filename = f"logs/resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            
            self.log(f"PIPELINE COMPLETADO - Resultado guardado en {filename}")
            self.log(f"Partidos: {result['data_stage']['total_matches']}")
            self.log(f"Predicciones: {result['harpo_stage']['total_predictions']}")
            self.log(f"Órdenes: {result['gambler_stage']['total_orders']}")
            
        except Exception as e:
            self.log(f"ERROR EN PIPELINE: {str(e)}")
    
    def schedule_jobs(self):
        """Configurar trabajos programados"""
        # Viernes, Sábado, Domingo
        days = ['friday', 'saturday', 'sunday']
        times = ['10:00', '14:00', '18:00', '21:00']
        
        for day in days:
            for time_str in times:
                schedule.every().day_of_week(
                    day_index=days.index(day)
                ).at(time_str).do(self.job_pipeline)
        
        self.log("Trabajos programados para Viernes, Sábado, Domingo")
        self.log(f"Horarios: {', '.join(times)}")
    
    def run(self):
        """Ejecutar scheduler"""
        self.log("\n" + "="*70)
        self.log("SCHEDULER DE PRONOSTICOS - INICIADO")
        self.log("="*70)
        
        self.schedule_jobs()
        
        self.log("Esperando horarios programados...")
        self.log("(Presiona Ctrl+C para detener)\n")
        
        # Loop infinito
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar cada minuto
        except KeyboardInterrupt:
            self.log("\nSCHEDULER DETENIDO POR EL USUARIO")

if __name__ == "__main__":
    scheduler = SchedulerPronosticos()
    scheduler.run()
