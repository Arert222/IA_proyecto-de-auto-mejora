import json
import random
from typing import List, Dict
from .main import AICoder
from .complexity_analyzer import ComplexityAnalyzer

class PeerReviewSystem:
    def __init__(self, agent_profiles: str = "agents/agent_profiles.json"):
        self.agents = self._load_agents(agent_profiles)
        self.competition_log = "peer_reviews.json"
        self.analyzer = ComplexityAnalyzer()
    
    def _load_agents(self, profile_path: str) -> List[AICoder]:
        """Carga diferentes agentes con personalidades únicas"""
        with open(profile_path) as f:
            profiles = json.load(f)
        
        return [
            AICoder(
                model_name=profile["model"],
                temperature=profile["temperature"],
                max_length=profile["max_length"]
            ) for profile in profiles["agents"]
        ]
    
    def code_competition(self, prompt: str, rounds: int = 3) -> Dict:
        """Ejecuta una competencia de codificación entre agentes"""
        solutions = []
        
        for _ in range(rounds):
            # Cada agente genera una solución
            solutions += [{
                "agent": agent,
                "code": agent.generate_optimal_code(prompt),
                "score": 0
            } for agent in self.agents]
            
            # Evaluación cruzada
            for solution in solutions:
                evaluators = random.sample(self.agents, 2)
                solution["score"] += self._evaluate_solution(
                    solution["code"], 
                    evaluators,
                    prompt
                )
        
        # Seleccionar mejor solución
        best_solution = max(solutions, key=lambda x: x["score"])
        self._log_competition(best_solution)
        return best_solution
    
    def _evaluate_solution(self, code: str, evaluators: List[AICoder], prompt: str) -> float:
        """Evaluación por múltiples agentes"""
        scores = []
        
        for evaluator in evaluators:
            critique = evaluator.generate_code(
                f"""Evalúa este código basado en:
                - Correctitud (40%)
                - Eficiencia (30%)
                - Legibilidad (30%)
                
                Código: {code}
                
                Requerimiento original: {prompt}
                
                Da un puntaje total del 1 al 10 y una explicación breve:"""
            )
            
            try:
                score = float(critique.split("Puntaje: ")[1].split("/10")[0])
                scores.append(score)
            except:
                scores.append(random.uniform(5.0, 8.0))
        
        return sum(scores) / len(scores)
    
    def _log_competition(self, solution: Dict):
        """Registra resultados de la competencia"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "code": solution["code"],
            "score": solution["score"],
            "metrics": self.analyzer.analyze(solution["code"])
        }
        
        with open(self.competition_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")