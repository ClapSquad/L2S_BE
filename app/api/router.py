from app.api.router_base import routers
import pkgutil, importlib
import app.api


def init_router(package):
    package_path = package.__path__
    module_name = package.__name__

    for module_info in pkgutil.iter_modules(package_path):
        name = module_info.name
        full_module = f"{module_name}.{name}"

        module = importlib.import_module(full_module)

        if hasattr(module, "__path__"):
            init_router(module)


def add_router(application):
    init_router(app.api)
    for router in routers:
        application.include_router(router)