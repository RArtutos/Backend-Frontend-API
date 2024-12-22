from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, accounts, proxies, analytics, sessions, delete
from .routers.admin import users, analytics as admin_analytics, presets, accounts as admin_accounts
from .core.config import settings
from .db.repositories.session_repository import SessionRepository
from datetime import datetime, timedelta
import asyncio
import json
import logging
import os
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Account Manager API")

# Update CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(proxies.router, prefix="/api/proxies", tags=["proxies"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(users.router, prefix="/api/admin/users", tags=["admin-users"])
app.include_router(admin_analytics.router, prefix="/api/admin/analytics", tags=["admin-analytics"])
app.include_router(presets.router, prefix="/api/admin/presets", tags=["admin-presets"])
app.include_router(admin_accounts.router, prefix="/api/admin/accounts", tags=["admin-accounts"])
app.include_router(delete.router, prefix="/delete", tags=["delete"])

session_repo = SessionRepository()

HISTORY_FILE = "data/sessions_history.json"
MAX_HISTORY_DAYS = 60  # 2 meses

async def capture_session_history():
    """Captura el estado actual de las sesiones y lo guarda en el historial"""
    while True:
        try:
            # Asegurarse que el directorio data existe
            Path("data").mkdir(exist_ok=True)

            # Cargar historial existente
            history = []
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)

            # Obtener datos actuales
            with open(settings.DATA_FILE, 'r') as f:
                data = json.load(f)
                current_sessions = data.get("sessions", [])
                accounts = data.get("accounts", [])

            # Crear snapshot
            snapshot = {
                "timestamp": datetime.utcnow().isoformat(),
                "total_sessions": len(current_sessions),
                "active_sessions": len([s for s in current_sessions if s.get("active", False)]),
                "accounts_data": []
            }

            # Procesar datos por cuenta
            for account in accounts:
                account_sessions = [s for s in current_sessions if s.get("account_id") == account["id"]]
                account_data = {
                    "account_id": account["id"],
                    "name": account["name"],
                    "total_sessions": len(account_sessions),
                    "active_sessions": len([s for s in account_sessions if s.get("active", False)]),
                    "unique_users": len(set(s["user_id"] for s in account_sessions)),
                    "domains": {}
                }

                # Contar sesiones por dominio
                for session in account_sessions:
                    domain = session.get("domain")
                    if domain:
                        if domain not in account_data["domains"]:
                            account_data["domains"][domain] = 0
                        account_data["domains"][domain] += 1

                snapshot["accounts_data"].append(account_data)

            # Agregar snapshot al historial
            history.append(snapshot)

            # Mantener solo los últimos MAX_HISTORY_DAYS días
            cutoff_date = datetime.utcnow() - timedelta(days=MAX_HISTORY_DAYS)
            history = [h for h in history if datetime.fromisoformat(h["timestamp"]) > cutoff_date]

            # Guardar historial actualizado
            with open(HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)

            logging.info(f"Session history captured at {snapshot['timestamp']}")

        except Exception as e:
            logging.error(f"Error capturing session history: {e}")

        await asyncio.sleep(60)  # Esperar 1 minuto

async def cleanup_expired_and_deleted_users():
    while True:
        try:
            logging.info("Starting cleanup process...")
            with open(settings.DATA_FILE, 'r') as f:
                data = json.load(f)

            modified = False

            # Verificar usuarios expirados
            for user in data.get("users", []):
                if user.get("expires_at"):
                    expires_at = datetime.fromisoformat(user["expires_at"])
                    if datetime.utcnow() > expires_at:
                        logging.info(f"User {user['email']} has expired.")
                        sessions_to_remove = [
                            session for session in data.get("sessions", [])
                            if session.get("user_id") == user["email"] and session.get("active")
                        ]
                        for session in sessions_to_remove:
                            if session_repo.delete_session(session["id"]):
                                modified = True

            # Verificar usuarios eliminados
            user_emails = {user["email"] for user in data.get("users", [])}
            sessions_to_remove = [
                session for session in data.get("sessions", [])
                if session.get("user_id") not in user_emails and session.get("active")
            ]
            for session in sessions_to_remove:
                logging.info(f"Session for user {session['user_id']} is inactive as user is deleted.")
                if session_repo.delete_session(session["id"]):
                    modified = True

            if modified:
                logging.info("Cleanup process completed and data file updated successfully.")
        except Exception as e:
            logging.error(f"Error in cleanup_expired_and_deleted_users: {e}")

        await asyncio.sleep(120)  # Esperar 2 minutos

@app.on_event("startup")
async def startup_event():
    settings.init_data_file()
    asyncio.create_task(cleanup_expired_and_deleted_users())
    asyncio.create_task(capture_session_history())
