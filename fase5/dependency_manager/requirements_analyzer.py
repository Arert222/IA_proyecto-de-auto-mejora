import ast
import subprocess
from packaging.requirements import Requirement

class DependencyManager:
    def __init__(self, ai_core):
        self.ai = ai_core
        self.dependency_db = "dependency_knowledge.json"
    
    def analyze_code_dependencies(self, code: str) -> list:
        """Detecta dependencias necesarias"""
        tree = ast.parse(code)
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        
        return self._resolve_versions(list(imports))
    
    def _resolve_versions(self, packages: list) -> dict:
        """Encuentra versiones compatibles usando IA"""
        prompt = f"""Dado estos paquetes: {', '.join(packages)}
        Genera un requirements.txt con versiones compatibles
        Considera:
        - Últimas versiones estables
        - Compatibilidad entre paquetes
        - Restricciones del sistema"""
        
        return self.ai.generate_code(prompt)

    def auto_install(self, code: str):
        """Instala dependencias automáticamente"""
        requirements = self.analyze_code_dependencies(code)
        with open("temp_requirements.txt", "w") as f:
            f.write(requirements)
        
        subprocess.run(
            ["pip", "install", "-r", "temp_requirements.txt"],
            check=True
        )