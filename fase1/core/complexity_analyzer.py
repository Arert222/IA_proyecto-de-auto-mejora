import ast
import json
from datetime import datetime
import astunparse
import networkx as nx
import matplotlib.pyplot as plt

class ComplexityAnalyzer:
    def __init__(self):
        self.complexity_db = "complexity_knowledge.json"
        self.optimal_solutions = {
            "sorting": "O(n log n)",
            "search": "O(log n)",
            "fibonacci": "O(n)"
        }
    
    def analyze(self, code: str) -> dict:
        """Analiza complejidad del código"""
        parsed = ast.parse(code)
        metrics = {
            "time_complexity": self._calculate_time_complexity(parsed),
            "space_complexity": self._calculate_space_complexity(parsed),
            "optimality": self._check_optimality(parsed),
            "graph": self._generate_control_flow_graph(code),
            "timestamp": datetime.now().isoformat()
        }
        self._save_analysis(metrics)
        return metrics
    
    def _calculate_time_complexity(self, node) -> str:
        """Calcula complejidad temporal usando análisis AST"""
        loop_depth = 0
        complexity = "O(1)"
        
        for n in ast.walk(node):
            if isinstance(n, (ast.For, ast.While, ast.AsyncFor)):
                loop_depth += 1
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'recursive_function':
                loop_depth += 2
        
        if loop_depth == 1:
            complexity = "O(n)"
        elif loop_depth == 2:
            complexity = "O(n^2)"
        elif loop_depth > 2:
            complexity = f"O(n^{loop_depth})"
        
        return complexity
    
    def _calculate_space_complexity(self, node) -> str:
        """Calcula complejidad espacial"""
        data_structures = set()
        
        for n in ast.walk(node):
            if isinstance(n, ast.List):
                data_structures.add("list")
            elif isinstance(n, ast.Dict):
                data_structures.add("dict")
            elif isinstance(n, ast.Set):
                data_structures.add("set")
        
        if "dict" in data_structures:
            return "O(n)"
        elif len(data_structures) > 2:
            return "O(n^2)"
        return "O(1)"
    
    def _check_optimality(self, node) -> float:
        """Compara con soluciones óptimas"""
        code_str = astunparse.unparse(node)
        optimal_score = 0.0
        
        for pattern, complexity in self.optimal_solutions.items():
            if pattern in code_str:
                current_complexity = self._calculate_time_complexity(node)
                optimal_score = 1.0 if current_complexity == complexity else 0.5
                break
        
        return optimal_score
    
    def _generate_control_flow_graph(self, code: str):
        """Genera gráfico de flujo de control"""
        graph = nx.DiGraph()
        lines = code.split('\n')
        
        for i, line in enumerate(lines[:-1]):
            graph.add_edge(i+1, i+2, label=line.strip())
        
        return nx.node_link_data(graph)
    
    def _save_analysis(self, metrics: dict):
        """Guarda análisis en JSON"""
        try:
            with open(self.complexity_db, 'r+') as f:
                data = json.load(f)
                data.append(metrics)
                f.seek(0)
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            with open(self.complexity_db, 'w') as f:
                json.dump([metrics], f, indent=2)
    
    def plot_evolution(self):
        """Muestra gráfico de evolución de complejidad"""
        with open(self.complexity_db, 'r') as f:
            data = json.load(f)
        
        scores = [entry['optimality'] for entry in data]
        plt.plot(scores, marker='o')
        plt.title('Evolución de la Optimalidad del Código')
        plt.ylabel('Puntuación de Optimalidad')
        plt.xlabel('Iteraciones')
        plt.grid(True)
        plt.show()