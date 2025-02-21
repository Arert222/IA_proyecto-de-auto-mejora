from ai_coder.main import AICoder
from ai_coder.complexity_analyzer import ComplexityAnalyzer

def main():
    # Inicializar componentes
    coder = AICoder()
    analyzer = ComplexityAnalyzer()
    
    # Generar código óptimo
    prompt = "Implementa una función de ordenamiento eficiente"
    code = coder.generate_optimal_code(prompt)
    
    print("Código Generado:")
    print(code)
    
    # Analizar y mostrar resultados
    analysis = analyzer.analyze(code)
    print("\nAnálisis de Complejidad:")
    print(f"Temporal: {analysis['time_complexity']}")
    print(f"Espacial: {analysis['space_complexity']}")
    print(f"Optimalidad: {analysis['optimality']*100:.1f}%")
    
    # Mostrar evolución
    analyzer.plot_evolution()

if __name__ == "__main__":
    main()