import ast

class ThreatDetector:
    def scan(self, code: str) -> list:
        """Detecta patrones peligrosos"""
        threats = []
        for node in ast.walk(ast.parse(code)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ["eval", "exec", "open"]:
                    threats.append(f"Uso peligroso de {node.func.id}")
        return threats