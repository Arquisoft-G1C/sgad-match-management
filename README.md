# SGAD – Match Management Service

Microservicio del **SGAD (Sistema de Gestión de Árbitros y Designaciones)** encargado de la **gestión de partidos**.  
Permite crear, consultar, actualizar y eliminar información de partidos, y se integra con el sistema central a través del **API Gateway**.

---

## 📖 Descripción

El **Match Management Service** administra toda la información relacionada con los partidos:  
- Registro de partidos.  
- Actualización de datos de partidos.  
- Consulta de partidos existentes.  
- Eliminación de registros.  
- Validación de disponibilidad de árbitros antes de la asignación.  

Este servicio expone **endpoints REST** que son consumidos por el **API Gateway** del sistema SGAD.

---

## 📂 Estructura del Proyecto

```
sgad-match-management/
│── .env                  # Variables de entorno (ejemplo: URL de la base de datos)
│── requirements.txt       # Dependencias de Python
│
└── app/
    ├── __init__.py
    ├── main.py            # Punto de entrada (endpoints)
    ├── crud.py            # Funciones CRUD sobre partidos
    ├── database.py        # Configuración de conexión a PostgreSQL
    ├── models.py          # Definición de modelos ORM (SQLAlchemy)
    ├── schemas.py         # Validaciones y serialización (Pydantic)
```

---

## ⚙️ Requisitos

- **Python 3.9+**
- **PostgreSQL** como base de datos relacional
- Docker (opcional, para despliegue contenerizado)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución Local

1. Configurar las variables de entorno en un archivo `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sgad_matches
```

2. Ejecutar el servidor en modo desarrollo:

```bash
uvicorn app.main:app --reload
```

3. La API estará disponible en:

- Base URL: `http://localhost:8001`
- Documentación automática (Swagger): `http://localhost:8001/docs`

---

## 🔗 Endpoints Principales

| Método | Endpoint            | Descripción                     |
|--------|--------------------|---------------------------------|
| GET    | `/matches`         | Listar todos los partidos       |
| GET    | `/matches/{id}`    | Obtener un partido por ID       |
| POST   | `/matches`         | Crear un nuevo partido          |
| PUT    | `/matches/{id}`    | Actualizar un partido existente |
| DELETE | `/matches/{id}`    | Eliminar un partido             |

---

## 🐳 Despliegue con Docker

1. Crear la imagen:
```bash
docker build -t sgad-match-management .
```

2. Ejecutar el contenedor:
```bash
docker run -d -p 8001:8000 --env-file .env sgad-match-management
```

---

## 📡 Integración con SGAD

- Este servicio se comunica con el **API Gateway** (`sgad-api-gateway`).  
- La información de partidos es persistida en **PostgreSQL** (contenedor `relational-db` en `sgad-main`).  
- Trabaja en conjunto con el microservicio **Referee Management** para la asignación de árbitros.

---
