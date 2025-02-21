from transformers import AutoTokenizer, AutoModelForCausalLM
from .complexity_analyzer import ComplexityAnalyzer
import torch

class AICoder:
    def __init__(self, model_name="microsoft/phi-3-mini-4k-instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.analyzer = ComplexityAnalyzer()
    
    def generate_optimal_code(self, prompt: str, max_complexity: str = "O(n log n)") -> str:
        """Genera código optimizado con restricciones de complejidad"""
        for _ in range(3):  # 3 intentos de optimización
            code = self._generate_code(prompt, max_complexity)
            analysis = self.analyzer.analyze(code)
            
            if analysis['optimality'] >= 0.8:
                return code
            
            prompt = f"{prompt}\nOptimiza este código para complejidad {max_complexity}:\n{code}"
        
        return code
    
    def _generate_code(self, prompt: str, constraints: str) -> str:
        """Generación base con restricciones"""
        full_prompt = f"""
        [REQUERIMIENTO]
        {prompt}
        
        [RESTRICCIONES]
        - Complejidad temporal: {constraints}
        - Uso eficiente de memoria
        - Estilo PEP8
        """
        
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=500)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)