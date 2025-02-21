import json
import ast
from typing import List, Dict
from .peer_review import PeerReviewSystem
from .complexity_analyzer import ComplexityAnalyzer

class DebateManager:
    def __init__(self, max_rounds: int = 3, consensus_threshold: float = 0.8):
        self.review_system = PeerReviewSystem()
        self.analyzer = ComplexityAnalyzer()
        self.max_rounds = max_rounds
        self.consensus_threshold = consensus_threshold
        self.debate_log = []

    def conduct_debate(self, prompt: str) -> Dict:
        """Coordina un debate completo entre agentes"""
        initial_solutions = self.review_system.code_competition(prompt, rounds=1)
        debate_rounds = []

        for round in range(self.max_rounds):
            round_data = {
                "round": round + 1,
                "arguments": [],
                "rebuttals": [],
                "solutions": []
            }

            # Fase de argumentación
            for solution in initial_solutions:
                critique = self._generate_critique(solution['code'], prompt)
                round_data["arguments"].append(critique)

            # Fase de refutación
            for agent in self.review_system.agents:
                rebuttal = self._generate_rebuttal(round_data["arguments"], agent)
                round_data["rebuttals"].append(rebuttal)

            # Fase de refinamiento
            refined_solutions = []
            for agent in self.review_system.agents:
                new_code = agent.generate_code(
                    f"{prompt}\n[CRÍTICAS RECIBIDAS]\n{round_data['rebuttals']}"
                )
                refined_solutions.append({
                    "agent": agent,
                    "code": new_code,
                    "score": self.analyzer.analyze(new_code)['optimality']
                })

            round_data["solutions"] = refined_solutions
            debate_rounds.append(round_data)

            if self._check_consensus(refined_solutions):
                break

        best_solution = max(refined_solutions, key=lambda x: x['score'])
        self._log_debate(prompt, debate_rounds, best_solution)
        return best_solution

    def _generate_critique(self, code: str, prompt: str) -> List[str]:
        """Genera críticas estructuradas desde múltiples perspectivas"""
        critique_template = """Analiza el siguiente código desde la perspectiva de {role}:
        - Puntos fuertes (20%)
        - Debilidades (50%)
        - Sugerencias de mejora (30%)
        
        Código: {code}
        Requerimiento original: {prompt}"""

        critiques = []
        for role in ["experto en seguridad", "ingeniero de rendimiento", "desarrollador senior"]:
            critique_prompt = critique_template.format(role=role, code=code, prompt=prompt)
            critiques.append(self.review_system.agents[0].generate_code(critique_prompt))
        
        return critiques

    def _generate_rebuttal(self, arguments: List[str], agent: AICoder) -> str:
        """Genera contraargumentos basados en las críticas"""
        rebuttal_prompt = f"""Como {agent.profile['name']}, responde a estas críticas:
        {arguments}
        
        Enfócate en:
        - Defender decisiones clave
        - Proponer mejoras concretas
        - Mantener profesionalismo"""
        
        return agent.generate_code(rebuttal_prompt)

    def _check_consensus(self, solutions: List[Dict]) -> bool:
        """Determina si hay consenso entre las soluciones"""
        scores = [sol['score'] for sol in solutions]
        avg_score = sum(scores) / len(scores)
        return (max(scores) - min(scores)) < (1 - self.consensus_threshold)

    def _log_debate(self, prompt: str, rounds: List[Dict], winner: Dict):
        """Registra todo el debate con formato estructurado"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "rounds": rounds,
            "winner": winner,
            "metrics": self.analyzer.analyze(winner['code'])
        }

        with open("debates.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def visualize_debate(self, debate_id: int):
        """Genera visualización interactiva del debate"""
        # Implementar con Plotly o similar
        pass