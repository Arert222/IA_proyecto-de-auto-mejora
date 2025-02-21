Instrucciones de Uso
Copia la estructura de carpetas en tu proyecto.

Instala dependencias:

bash
Copy
pip install -r requirements-phase6.txt
Ejecuta pruebas:

bash
Copy
python -m pytest tests/ -v
Integración con Fases Anteriores
Modifica tu archivo principal (main.py):

python
Copy
# Añade al inicio
from fase6.project_management.time_estimator import TimeEstimator
from fase6.security.sandbox import CodeSandbox

class SelfImprovingAIProgrammer:
    def __init__(self):
        # ... (código anterior)
        self.estimator = TimeEstimator()
        self.sandbox = CodeSandbox()