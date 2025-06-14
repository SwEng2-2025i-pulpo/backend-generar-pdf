# 🧾 Servicio de Generación de PDF - ConectaCare

Este servicio permite generar un reporte en PDF del perfil de un paciente desde la base de datos de MongoDB. Está construido con **FastAPI** y devuelve el archivo como respuesta descargable.

---

## 🚀 Tecnologías utilizadas

- **FastAPI** - Framework web moderno y rápido para APIs
- **MongoDB** - Base de datos NoSQL
- **Pymongo** - Cliente MongoDB para Python
- **ReportLab / FPDF / WeasyPrint** (según la librería usada en `pdf_service`) - Generación del PDF

---

## 📁 Estructura del proyecto

.
├── services/
│ └── pdf_service.py # Lógica para construir el PDF con los datos del paciente
├── routes/
│ └── pdf.py # Ruta que expone el endpoint para descargar el PDF
├── main.py # Archivo principal de FastAPI
├── models/
│ └── patient.py # Modelo de datos del paciente


---

## 🔌 Endpoint disponible

### `GET /patient/{patient_id}`

#### 📥 Parámetros:

- `patient_id` (path): ID del paciente en formato MongoDB ObjectId.

#### 📤 Respuesta:

- `200 OK`: PDF descargable con los datos del paciente.
- `400`: ID inválido.
- `404`: Paciente no encontrado.
- `500`: Error interno del servidor.

### Configuración inicial

git clone https://github.com/tuusuario/conectacare-backend.git
cd conectacare-backend

### Crea un entorno virtual y actívalo:

python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

### Instala dependencias
pip install -r requirements.txt

### Ejecuta el servidor

uvicorn main:app --reload


#### 🧪 Ejemplo de uso:


```bash
curl -X GET http://localhost:8000/patient/66486fe15fa223334db17bdf --output paciente.pdf



