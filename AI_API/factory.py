from django.conf import settings
from typing import Optional

from .ports import AIGenerationClient
from .services import Gemma3Service
from .mock_service import MockAIService


def create_ai_client(provider: Optional[str] = None, use_fallback: bool = True) -> AIGenerationClient:
    """
    Simple Factory que devuelve una estrategia de cliente de IA según configuración.
    Usa Strategy a través del puerto AIGenerationClient.
    
    settings.AI_PROVIDER puede ser: 'gemma' (default), 'openai', 'mock', etc.
    """
    selected = (provider or getattr(settings, 'AI_PROVIDER', 'gemma') or 'gemma').lower()

    if selected == 'openai':
        try:
            from .openai_service import OpenAIService  # import local, opcional
            return OpenAIService()
        except Exception:
            # Fallback seguro si el adaptador alterno no está disponible
            return Gemma3Service()
    elif selected == 'mock':
        return MockAIService()
    elif selected == 'clientpy':
        from .client_py_adapter import ClientPyAdapter
        return ClientPyAdapter()

    # Por defecto usa Gemma3Service, pero con fallback a mock si falla
    if use_fallback:
        try:
            # Probar si el servicio principal funciona
            service = Gemma3Service()
            health = service.health_check()
            if health.get('status') == 'healthy':
                return service
            else:
                print("⚠️ Servicio principal no disponible, usando mock service")
                return MockAIService()
        except Exception as e:
            print(f"⚠️ Error con servicio principal: {e}, usando mock service")
            return MockAIService()
    
    # Sin fallback, usar servicio principal directamente
    return Gemma3Service()


