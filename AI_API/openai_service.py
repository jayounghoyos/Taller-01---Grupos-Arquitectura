from typing import Dict, Any, List, Optional

# Stub que implementa el puerto AIGenerationClient sin dependencias reales.
# Útil para ilustrar Strategy y para tests sin consumir API externa.


class OpenAIService:
    def __init__(self):
        # Aquí iría configuración real (keys, endpoints)
        pass

    def generate_response(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        request_type: str = "chat",
        user: Any = None,
    ) -> Dict[str, Any]:
        # Respuesta simulada compatible con ProductAIService
        return {
            "success": True,
            "response": '{"title": "Demo OpenAI", "description": "Desc generada", "suggested_category": "Hogar", "tags": "tag1, tag2", "price_suggestion": "20"}',
            "tokens_used": 42,
            "processing_time": 0.01,
            "request_id": None,
            "model": "openai/stub",
        }

    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "provider": "openai-stub"}


