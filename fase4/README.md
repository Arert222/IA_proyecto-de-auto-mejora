sequenceDiagram
    participant Usuario
    participant VSCode
    participant LSP_Server
    participant IA_Core
    
    Usuario->>VSCode: Escribe código
    VSCode->>LSP_Server: Solicita sugerencias
    LSP_Server->>IA_Core: Genera código
    IA_Core->>LSP_Server: Devuelve sugerencia
    LSP_Server->>VSCode: Muestra sugerencia
    Usuario->>VSCode: Califica sugerencia (1-5 estrellas)
    VSCode->>LSP_Server: Envía retroalimentación
    LSP_Server->>FeedbackProcessor: Procesa feedback
    FeedbackProcessor->>IA_Core: Actualiza modelo


 Para Implementar:


Instala dependencias:

bash

pip install -r requirements-phase4.txt

Inicia el servidor LSP:

python

from lsp_server import CodeAssistantServer
from main import SelfImprovingAIProgrammer

ai = SelfImprovingAIProgrammer()
server = CodeAssistantServer(ai)
server.start()
Configura la extensión de VSCode (archivo package.json):

json

{
    "name": "ai-code-assistant",
    "activationEvents": ["onLanguage:python"],
    "contributes": {
        "configuration": {
            "title": "AI Assistant",
            "properties": {
                "aiAssistant.enable": {"type": "boolean", "default": true}
            }
        }
    }
}
   