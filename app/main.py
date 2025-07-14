from fastapi import FastAPI, Request
from fastapi.responses import Response
from routes.pdf import pdf_router
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time


app = FastAPI()

app.include_router(pdf_router, prefix="/api/pdf")

# Configuración de CORS
origins = [
    "http://localhost:3000",  # React local
    "http://localhost:5173",
    # Añadir otros orígenes aquí, como el dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origenes permitidos
    allow_credentials=True,
    allow_methods=["*"],    # Métodos permitidos
    allow_headers=["*"],    # Encabezados permitidos
)

# Métricas Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total", "Total de peticiones HTTP", ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Duración de la petición en segundos", ["method", "endpoint"]
)

EXCEPTIONS_COUNT = Counter(
    "http_exceptions_total", "Conteo de excepciones por endpoint", ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        EXCEPTIONS_COUNT.labels(method=method, endpoint=endpoint).inc()
        status_code = 500
        raise

    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



# uvicorn main:app --reload --port 8001

