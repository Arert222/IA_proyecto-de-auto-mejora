import jsonrpc
from jsonrpc import JSONRPCServer
from threading import Thread

class CodeAssistantServer:
    def __init__(self, ai_programmer):
        self.ai = ai_programmer
        self.server = JSONRPCServer(('localhost', 2087))
        self.server.register_function(self.get_suggestions)
        self.server.register_function(self.submit_feedback)

    def get_suggestions(self, code_context: str) -> list:
        """Provee sugerencias en tiempo real"""
        prompt = f"Contexto actual:\n{code_context}\nSugerencia:"
        suggestion = self.ai.generate_code(prompt, max_retries=1)
        return [{
            "range": {"start": {"line": 0, "character": 0},
                      "end": {"line": 0, "character": 0}},
            "text": suggestion,
            "type": "quickfix"
        }]

    def submit_feedback(self, code: str, feedback: dict):
        """Procesa retroalimentación humana"""
        self.ai._update_json("human_feedback_db.json", {
            "timestamp": datetime.now().isoformat(),
            "code": code,
            "rating": feedback["rating"],
            "comments": feedback["comments"]
        })
        return {"status": "feedback processed"}

    def start(self):
        """Inicia el servidor LSP"""
        Thread(target=self.server.serve_forever).start()