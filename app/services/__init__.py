"""
CAMADA DE SERVIÇOS = classes/arquivos que contêm os ENDPOINTS (termo do professor).

Para criar um novo módulo: crie `app/services/<nome>_service.py` com uma variável
`bp = Blueprint(...)`. Ele é registrado AUTOMATICAMENTE (não precisa mexer aqui).
"""
import importlib
import pkgutil


def registrar_services(app):
    for modulo_info in pkgutil.iter_modules(__path__):
        modulo = importlib.import_module(f"{__name__}.{modulo_info.name}")
        blueprint = getattr(modulo, "bp", None)
        if blueprint is not None:
            app.register_blueprint(blueprint)
