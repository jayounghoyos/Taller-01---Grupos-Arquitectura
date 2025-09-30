#!/usr/bin/env python3
"""
Servicio de IA Mock para desarrollo y testing
"""

import json
import time
import random
from typing import Dict, List, Any, Optional

class MockAIService:
    """
    Servicio Mock de IA que simula respuestas sin hacer llamadas reales
    Útil para desarrollo y testing cuando el servidor Lightning AI no está disponible
    """
    
    def __init__(self):
        self.model_name = "mock-gemma-3-4b-it"
        self.max_tokens = 256
        self.temperature = 0.7
    
    def generate_response(self, prompt: str, image_urls: List[str] = None,
                        max_tokens: int = None, temperature: float = None,
                        request_type: str = 'chat', user=None) -> Dict[str, Any]:
        """
        Genera una respuesta mock basada en el prompt
        """
        start_time = time.time()
        
        # Simular tiempo de procesamiento
        processing_time = random.uniform(1.0, 3.0)
        time.sleep(min(processing_time, 0.1))  # Solo sleep real si es muy corto
        
        # Generar respuesta basada en el tipo de request
        if request_type == 'product_analysis':
            response = self._generate_product_analysis()
        elif 'product' in prompt.lower():
            response = self._generate_product_response()
        else:
            response = self._generate_general_response(prompt)
        
        return {
            'success': True,
            'response': response,
            'tokens_used': random.randint(50, 200),
            'processing_time': processing_time,
            'request_id': f"mock_{int(time.time())}",
            'model': self.model_name
        }
    
    def _generate_product_analysis(self) -> str:
        """Genera análisis de producto mock"""
        return json.dumps({
            "title": "Camisa Casual de Algodón",
            "description": "Camisa de algodón 100% natural, perfecta para uso diario. Diseño clásico con cuello tipo polo y botones frontales. Ideal para oficina o eventos casuales. Disponible en múltiples colores.",
            "suggested_category": "Ropa",
            "tags": "camisa, algodón, casual, polo, oficina, ropa",
            "price_suggestion": "25.99"
        }, ensure_ascii=False)
    
    def _generate_product_response(self) -> str:
        """Genera respuesta relacionada con productos"""
        responses = [
            "Este producto parece ser una prenda de vestir de buena calidad.",
            "La imagen muestra un artículo de moda con características atractivas.",
            "Producto bien diseñado, ideal para el mercado objetivo.",
            "Excelente calidad y diseño, recomendado para venta online."
        ]
        return random.choice(responses)
    
    def _generate_general_response(self, prompt: str) -> str:
        """Genera respuesta general"""
        responses = [
            "Entiendo tu consulta. ¿En qué más puedo ayudarte?",
            "Gracias por tu pregunta. Aquí tienes una respuesta útil.",
            "Interesante pregunta. Aquí está mi análisis.",
            "Perfecto, aquí tienes la información que necesitas."
        ]
        return random.choice(responses)
    
    def health_check(self) -> Dict[str, Any]:
        """Health check mock"""
        return {
            'status': 'healthy',
            'model': self.model_name,
            'endpoint': 'mock-service',
            'message': 'Mock AI service is running'
        }

# Función para crear el cliente mock
def create_mock_ai_client():
    """Crea un cliente de IA mock"""
    return MockAIService()

if __name__ == "__main__":
    # Prueba del servicio mock
    service = MockAIService()
    
    print("=== Mock AI Service Test ===")
    
    # Probar health check
    health = service.health_check()
    print(f"Health: {health}")
    
    # Probar análisis de producto
    result = service.generate_response(
        prompt="Analiza este producto",
        image_urls=["test_image.jpg"],
        request_type="product_analysis"
    )
    print(f"Product analysis: {result}")
    
    print("✓ Mock service working!")
