import requests
import time
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import AIRequest, AIConfiguration
from .ports import AIGenerationClient
# Configuración directa desde settings
LIGHTNING_AI_ENDPOINT = getattr(settings, 'LIGHTNING_AI_ENDPOINT', 'https://8001-01k4ap2fswtrsc3fyamsj261fp.cloudspaces.litng.ai')
LIGHTNING_AI_API_KEY = getattr(settings, 'LIGHTNING_AI_API_KEY', 'gemma3-litserve')
MODEL_NAME = 'google/gemma-3-4b-it'
DEFAULT_MAX_TOKENS = 256
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TIMEOUT = 300

class Gemma3Service:
    """
    Servicio para interactuar con el modelo Gemma 3 desplegado en Lightning AI
    """
    
    def __init__(self):
        self.config = self._get_active_config()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.api_key}'
        })
    
    def _get_active_config(self) -> AIConfiguration:
        """Obtiene la configuración activa de IA"""
        try:
            config = AIConfiguration.objects.filter(is_active=True).first()
            if not config:
                # Crear configuración por defecto si no existe
                config = AIConfiguration.objects.create(
                    name='default',
                    lightning_endpoint=LIGHTNING_AI_ENDPOINT,
                    api_key=LIGHTNING_AI_API_KEY,
                    model_name=MODEL_NAME,
                    max_tokens_default=DEFAULT_MAX_TOKENS,
                    temperature_default=DEFAULT_TEMPERATURE,
                    timeout_seconds=DEFAULT_TIMEOUT
                )
            return config
        except Exception as e:
            
            raise
    
    def _build_messages(self, prompt: str, image_urls: List[str] = None) -> List[Dict]:
        """
        Construye el formato de mensajes compatible con OpenAI API
        """
        content = [{"type": "text", "text": prompt}]
        
        if image_urls:
            for image_url in image_urls:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_url}
                })
        
        return [{"role": "user", "content": content}]
    
    def _build_payload(self, prompt: str, image_urls: List[str] = None, 
                      max_tokens: int = None, temperature: float = None) -> Dict:
        """
        Construye el payload para la API de Gemma 3
        """
        return {
            "model": self.config.model_name,
            "messages": self._build_messages(prompt, image_urls),
            "max_tokens": max_tokens or self.config.max_tokens_default,
            "temperature": temperature or self.config.temperature_default,
            "stream": False
        }
    
    def generate_response(self, prompt: str, image_urls: List[str] = None,
                        max_tokens: int = None, temperature: float = None,
                        request_type: str = 'chat', user=None) -> Dict[str, Any]:
        """
        Genera una respuesta del modelo Gemma 3
        
        Args:
            prompt: Texto del prompt
            image_urls: Lista de URLs de imágenes (opcional)
            max_tokens: Máximo número de tokens (opcional)
            temperature: Temperatura para la generación (opcional)
            request_type: Tipo de request ('chat', 'product_description', etc.)
            user: Usuario que hace la request (opcional)
        
        Returns:
            Dict con la respuesta del modelo y metadatos
        """
        start_time = time.time()
        
        # Crear registro de request
        ai_request = AIRequest.objects.create(
            user=user,
            request_type=request_type,
            status='pending',
            prompt=prompt,
            image_urls=image_urls or [],
            model_name=self.config.model_name,
            max_tokens=max_tokens or self.config.max_tokens_default,
            temperature=temperature or self.config.temperature_default
        )
        
        try:
            # Actualizar estado a procesando
            ai_request.status = 'processing'
            ai_request.save()
            
            # Construir payload
            payload = self._build_payload(prompt, image_urls, max_tokens, temperature)
            
            # Hacer request al endpoint
            response = self.session.post(
                f"{self.config.lightning_endpoint}/v1/chat/completions",
                json=payload,
                timeout=self.config.timeout_seconds
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Procesar respuesta
            processing_time = time.time() - start_time
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                response_text = response_data['choices'][0]['message']['content']
                usage = response_data.get('usage', {})
                tokens_used = usage.get('total_tokens', 0)
                
                # Actualizar request con respuesta exitosa
                ai_request.status = 'completed'
                ai_request.response_text = response_text
                ai_request.response_tokens = tokens_used
                ai_request.processing_time = processing_time
                ai_request.save()
                
             
                return {
                    'success': True,
                    'response': response_text,
                    'tokens_used': tokens_used,
                    'processing_time': processing_time,
                    'request_id': ai_request.id,
                    'model': self.config.model_name
                }
            else:
                raise Exception("No valid response from model")
                
        except requests.exceptions.RequestException as e:
            processing_time = time.time() - start_time
            error_msg = f"Request error: {str(e)}"
            
            ai_request.status = 'failed'
            ai_request.error_message = error_msg
            ai_request.processing_time = processing_time
            ai_request.save()
            
            
            
            
            
            return {
                'success': False,
                'error': error_msg,
                'processing_time': processing_time,
                'request_id': ai_request.id
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Unexpected error: {str(e)}"
            
            ai_request.status = 'failed'
            ai_request.error_message = error_msg
            ai_request.processing_time = processing_time
            ai_request.save()
            
            
            
            
            
            return {
                'success': False,
                'error': error_msg,
                'processing_time': processing_time,
                'request_id': ai_request.id
            }
    
 
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica el estado del servicio de IA
        """
        try:
            response = self.session.get(
                f"{self.config.lightning_endpoint}/",
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'endpoint': self.config.lightning_endpoint,
                    'model': self.config.model_name,
                    'response': response.text
                }
            else:
                return {
                    'status': 'unhealthy',
                    'endpoint': self.config.lightning_endpoint,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'endpoint': self.config.lightning_endpoint,
                'error': str(e)
            }


class ProductAIService:
    """
    Servicio específico para funcionalidades de IA relacionadas con productos
    """
    
    def __init__(self, ai_client: Optional[AIGenerationClient] = None):
        # Inversión de dependencias: dependemos del puerto (AIGenerationClient)
        # y por defecto inyectamos el adaptador concreto Gemma3Service.
        self.ai_client: AIGenerationClient = ai_client or Gemma3Service()
    
    # Funciones individuales eliminadas - solo se usa analyze_product_complete()
    
    def analyze_product_complete(self, image_url: str, user=None) -> Dict[str, Any]:
        """
        Análisis completo de producto desde una imagen para auto-llenar formulario
        Genera título, descripción, categoría sugerida y tags automáticamente
        """
        prompt = """Analiza esta imagen de producto y genera información completa para un e-commerce. 
        Responde SOLO en formato JSON con la siguiente estructura exacta:
        {
            "title": "Título atractivo del producto (máximo 60 caracteres)",
            "description": "Descripción detallada y convincente del producto (máximo 200 palabras)",
            "suggested_category": "Categoría más apropiada para este producto (debe ser una de: Ropa, Electrónicos, Hogar, Deportes, Libros, Juguetes, Belleza, Automotriz, Jardín, Oficina)",
            "tags": "tag1, tag2, tag3, tag4, tag5",
            "price_suggestion": "Precio estimado en USD basado en el producto"
        }
        
        El título debe ser atractivo y optimizado para SEO.
        La descripción debe destacar características clave y beneficios.
        La categoría DEBE ser una de estas opciones exactas: Ropa, Electrónicos, Hogar, Deportes, Libros, Juguetes, Belleza, Automotriz, Jardín, Oficina.
        Los tags deben ser palabras clave útiles para búsqueda.
        El precio debe ser realista basado en el tipo de producto."""
        
        result = self.ai_client.generate_response(
            prompt=prompt,
            image_urls=[image_url],
            max_tokens=500,
            temperature=0.7,
            request_type='product_analysis',
            user=user
        )
        
        if result['success']:
            try:
                # Intentar parsear la respuesta como JSON
                import json
                response_text = result['response']
                
                # Limpiar la respuesta para extraer solo el JSON
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    json_text = response_text[json_start:json_end].strip()
                elif '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
                
                parsed_data = json.loads(json_text)
                
                return {
                    'success': True,
                    'data': parsed_data,
                    'request_id': result.get('request_id'),
                    'processing_time': result.get('processing_time')
                }
                
            except json.JSONDecodeError as e:
            
                return {
                    'success': False,
                    'error': 'Error procesando respuesta de IA',
                    'raw_response': result['response']
                }
        else:
            return result

    def health_check(self) -> Dict[str, Any]:
        """Exponer health-check del cliente inyectado."""
        return self.ai_client.health_check()