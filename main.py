import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Inicializamos la aplicación de FastAPI
app = FastAPI(title="Backend Control de Bots", version="1.0")

# --- 2. Configurar los permisos de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ideal para desarrollo y app web abierta)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Credenciales de Supabase 
# (En producción, esto se lee de variables de entorno de tu PC o de Render)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Creamos la instancia de conexión a Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error al conectar con Supabase: {e}")

# --- PASO 2.2: Endpoint para obtener todos los bots y su estado ---
@app.get("/api/bots")
def obtener_bots():
    try:
        # Hacemos una consulta a la tabla 'bots' trayendo todos sus campos
        response = supabase.table("bots").select("*").execute()
        
        # Supabase devuelve los datos en la propiedad .data
        return {
            "status": "success",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/usuarios/{usuario_id}/bots")
def obtener_bots_usuario(usuario_id: int):
    response = supabase.table("bots").select("*").eq("user_id", usuario_id).execute()
    return response.data

@app.post("/api/bots/{bot_id}/cambiar-estado")
def cambiar_estado_bot(bot_id: int, activo: bool):
    supabase.table("bots").update({"activo": activo}).eq("id", bot_id).execute()
    return {"status": "actualizado", "bot_id": bot_id, "activo": activo}    