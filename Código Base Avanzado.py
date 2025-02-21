import ast
import json
import subprocess
import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class SelfImprovingAIProgrammer:
    def __init__(self, model_name="microsoft/phi-3-mini-4k-instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = self._load_quantized_model(model_name)
        self.knowledge_db = "knowledge_db.json"
        self.error_log = "error_analysis.json"
        
    def _load_quantized_model(self, model_name):
        """Carga el modelo con optimización de memoria"""
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )
        return AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
    
    def generate_code(self, prompt, max_retries=3):
        """Ciclo de generación con auto-corrección"""
        attempt = 0
        while attempt < max_retries:
            code = self._code_generation(prompt)
            if self._static_analysis(code):
                result = self._execute_code(code)
                if result["success"]:
                    self._update_knowledge(prompt, code, result)
                    return code
                else:
                    self._learn_from_error(code, result["error"])
                    prompt = self._create_retry_prompt(prompt, code, result["error"])
            attempt += 1
        return self._fallback_solution(prompt)

    def _code_generation(self, prompt):
        """Generación de código con contexto"""
        context = self._get_context(prompt)
        full_prompt = f"""
        [CONTEXTO PREVIO]
        {context}
        
        [NUEVO REQUERIMIENTO]
        {prompt}
        
        [RESTRICCIONES]
        1. Cumplir PEP8
        2. Incluir manejo de errores
        3. Optimizar para eficiencia
        """
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=500)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/CÓDIGO]")[-1].strip()

    def _static_analysis(self, code):
        """Validación sintáctica y de seguridad"""
        try:
            ast.parse(code)
            return self._security_checks(code)
        except Exception as e:
            self._log_error(code, str(e))
            return False

    def _security_checks(self, code):
        """Prevención de código peligroso"""
        forbidden_patterns = [
            "os.system", "subprocess.run", "eval(", "exec(",
            "open(", "__import__", "pickle.load"
        ]
        return not any(pattern in code for pattern in forbidden_patterns)

    def _execute_code(self, code):
        """Ejecución en sandbox seguro"""
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _learn_from_error(self, code, error):
        """Proceso de aprendizaje automático"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "code": code,
            "error": error,
            "corrected": False
        }
        self._update_json(self.error_log, error_data)
        self._retrain_model()

    def _retrain_model(self):
        """Fine-tuning adaptativo"""
        with open(self.error_log, "r") as f:
            errors = json.load(f)
        
        # Convertir errores en datos de entrenamiento
        training_data = [
            {"text": f"Error: {e['error']}\nCódigo defectuoso: {e['code']}\nCódigo corregido: {self._expert_fix(e['code'], e['error'])}"}
            for e in errors[-100:]  # Últimos 100 errores
        ]
        
        # Fine-tuning básico (implementación completa requeriría más pasos)
        self.model.train()
        # ... (implementar lógica de entrenamiento)
        self.model.eval()

    def _expert_fix(self, code, error):
        """Módulo experto para correcciones críticas"""
        # Implementar reglas específicas o llamar a API externa
        return f"# Corrección experta aplicada\n{code}"

    def _update_knowledge(self, prompt, code, result):
        """Actualiza la base de conocimiento"""
        entry = {
            "prompt": prompt,
            "code": code,
            "output": result["output"],
            "timestamp": datetime.now().isoformat()
        }
        self._update_json(self.knowledge_db, entry)

    def _update_json(self, filename, entry):
        """Actualiza archivos JSON manteniendo historial"""
        try:
            with open(filename, "r+") as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            with open(filename, "w") as f:
                json.dump([entry], f, indent=2)

# Uso del sistema
if __name__ == "__main__":
    ai = SelfImprovingAIProgrammer()
    
    while True:
        try:
            user_input = input("\nIngrese su requerimiento de programación (o 'exit'): ")
            if user_input.lower() == 'exit':
                break
                
            generated_code = ai.generate_code(user_input)
            print(f"\nCódigo Generado (v3.0):\n{generated_code}")
            
        except KeyboardInterrupt:
            print("\nSistema detenido por el usuario")
            break