from app.api.health import healthcheck
from app.api.file import upload
from app.api.auth import register, login, logout, me
from app.api.admin import forceLogout
from app.api.videos import router as videos_router



def add_router(application):
    application.include_router(healthcheck.router)
    application.include_router(upload.router)

    application.include_router(register.router)
    application.include_router(login.router)
    application.include_router(logout.router)
    application.include_router(me.router)

    application.include_router(forceLogout.router)
    application.include_router(videos_router)
