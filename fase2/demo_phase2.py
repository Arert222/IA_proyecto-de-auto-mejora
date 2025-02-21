from ai_coder.peer_review import PeerReviewSystem
import matplotlib.pyplot as plt

def visualize_reviews():
    # Cargar datos de competencias
    with open("peer_reviews.json") as f:
        reviews = [json.loads(line) for line in f]
    
    # Preparar datos
    scores = [r["score"] for r in reviews]
    complexities = [r["metrics"]["time_complexity"] for r in reviews]
    
    # Crear gráficos
    fig, axs = plt.subplots(2)
    
    axs[0].plot(scores, 'g-o')
    axs[0].set_title('Evolución de Puntajes')
    
    axs[1].hist(complexities)
    axs[1].set_title('Distribución de Complejidad')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    system = PeerReviewSystem()
    challenge = "Implementa una búsqueda binaria eficiente"
    
    print("🏁 Iniciando Competencia de IA...")
    winner = system.code_competition(challenge)
    
    print("\n🏆 Mejor Solución:")
    print(winner["code"])
    print(f"\nPuntaje: {winner['score']:.2f}/10")
    
    visualize_reviews()