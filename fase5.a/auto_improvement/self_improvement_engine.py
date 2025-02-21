import ast
import timeit
import inspect
from code_metrics import calculate_cyclomatic_complexity

class SelfImprovementEngine:
    def __init__(self, ai_core):
        self.ai = ai_core
        self.improvement_log = "code_improvements.json"
    
    def optimize_code(self, code: str) -> str:
        """Ejecuta el pipeline completo de optimización"""
        original_metrics = self._analyze_code(code)
        
        # Generar variantes de mejora
        variants = self._generate_optimization_variants(code)
        
        # Evaluar y seleccionar la mejor versión
        best_code = code
        best_score = self._calculate_code_score(original_metrics)
        
        for variant in variants:
            if self._validate_variant(variant):
                variant_metrics = self._analyze_code(variant)
                variant_score = self._calculate_code_score(variant_metrics)
                
                if variant_score > best_score:
                    best_code = variant
                    best_score = variant_score
        
        if best_code != code:
            self._log_improvement(code, best_code, best_score)
            self._update_ai_model(best_code)
        
        return best_code

    def _generate_optimization_variants(self, code: str) -> list:
        """Genera posibles versiones mejoradas"""
        optimization_prompts = [
            f"Optimiza este código para eficiencia:\n{code}",
            f"Mejora la legibilidad manteniendo funcionalidad:\n{code}",
            f"Refactoriza este código aplicando patrones de diseño:\n{code}",
            f"Reduce la complejidad ciclomática de:\n{code}"
        ]
        
        return [self.ai.generate_code(prompt) for prompt in optimization_prompts]

    def _analyze_code(self, code: str) -> dict:
        """Calcula métricas clave de calidad"""
        return {
            "execution_time": self._measure_execution_time(code),
            "memory_usage": self._measure_memory_usage(code),
            "cyclomatic_complexity": calculate_cyclomatic_complexity(code),
            "pep8_compliance": self._check_pep8_compliance(code)
        }

    def _calculate_code_score(self, metrics: dict) -> float:
        """Calcula puntuación compuesta de calidad"""
        weights = {
            "execution_time": 0.4,
            "memory_usage": 0.3,
            "cyclomatic_complexity": 0.2,
            "pep8_compliance": 0.1
        }
        return sum(metrics[k] * weights[k] for k in weights)

    def _update_ai_model(self, improved_code: str):
        """Actualiza el modelo con el código mejorado"""
        training_data = {
            "original": self.ai.generate_code("Genera el código original para: " + improved_code),
            "improved": improved_code
        }
        self.ai._retrain_model([training_data])