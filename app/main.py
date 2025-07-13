from fastapi import FastAPI
from routes.pdf import pdf_router
from fastapi.middleware.cors import CORSMiddleware


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


# uvicorn main:app --reload --port 8001