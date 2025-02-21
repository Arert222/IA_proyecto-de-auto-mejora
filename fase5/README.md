Para Implementar:
Inicia el sistema de monitoreo:

python

monitor = PerformanceMonitor()
Thread(target=monitor.track_performance).start()
Lanza el dashboard:

bash

# Backend
uvicorn api.main:app --reload

# Frontend (desde otro terminal)
cd dashboard/ui
npm start