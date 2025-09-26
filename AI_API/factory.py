from django.conf import settings
from typing import Optional

from .ports import AIGenerationClient
from .services import Gemma3Service


def create_ai_client(provider: Optional[str] = None) -> AIGenerationClient:
    """
    Simple Factory que devuelve una estrategia de cliente de IA según configuración.
    Usa Strategy a través del puerto AIGenerationClient.
    
    settings.AI_PROVIDER puede ser: 'gemma' (default), 'openai', etc.
    """
    selected = (provider or getattr(settings, 'AI_PROVIDER', 'gemma') or 'gemma').lower()

    if selected == 'openai':
        try:
            from .openai_service import OpenAIService  # import local, opcional
            return OpenAIService()
        except Exception:
            # Fallback seguro si el adaptador alterno no está disponible
            return Gemma3Service()

    # Default / fallback
    return Gemma3Service()


