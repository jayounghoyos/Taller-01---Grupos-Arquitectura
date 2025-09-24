from typing import Protocol, List, Dict, Any, Optional


class AIGenerationClient(Protocol):
    """
    Puerto (interfaz) para cualquier cliente de generación de IA.
    """

    def generate_response(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        request_type: str = "chat",
        user: Any = None,
    ) -> Dict[str, Any]:
        ...

    def health_check(self) -> Dict[str, Any]:
        ...


