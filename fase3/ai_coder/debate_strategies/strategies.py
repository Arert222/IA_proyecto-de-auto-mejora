from typing import Dict

DEBATE_STRATEGIES = {
    "defensive": {
        "response_template": "Como experto en {focus}, destacaría que...",
        "counter_arguments": 3,
        "compromise_threshold": 0.7
    },
    "aggressive": {
        "response_template": "La propuesta actual falla en {focus} porque...",
        "counter_arguments": 5,
        "compromise_threshold": 0.9
    },
    "collaborative": {
        "response_template": "Podríamos combinar {focus} para mejorar...",
        "counter_arguments": 2,
        "compromise_threshold": 0.6
    }
}

def apply_strategy(agent_profile: Dict, arguments: List[str]) -> str:
    strategy = DEBATE_STRATEGIES[agent_profile["strategy"]]
    focus_areas = ", ".join(agent_profile["focus"])
    
    response = strategy["response_template"].format(focus=focus_areas)
    response += "\n".join(arguments[:strategy["counter_arguments"]])
    
    if len(arguments) > strategy["counter_arguments"]:
        response += f"\nAdemás, consideremos: {arguments[strategy['counter_arguments']}"
    
    return response