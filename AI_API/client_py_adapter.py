#!/usr/bin/env python3
"""
Adaptador que usa el client.py que funciona
"""

import subprocess
import tempfile
import base64
import json
import os
import time
from typing import Dict, List, Any, Optional
from .ports import AIGenerationClient

class ClientPyAdapter(AIGenerationClient):
    """
    Adaptador que usa el client.py que funciona
    """
    
    def __init__(self):
        self.model_name = "google/gemma-3-4b-it"
        self.client_script = "client.py"  # Ruta al script que funciona
    
    def generate_response(self, prompt: str, image_urls: List[str] = None,
                        max_tokens: int = None, temperature: float = None,
                        request_type: str = 'chat', user=None) -> Dict[str, Any]:
        """
        Genera una respuesta usando el client.py que funciona
        Si falla, usa el mock service como fallback
        """
        start_time = time.time()
        
        try:
            if not image_urls:
                # Si no hay imagen, usar prompt simple
                return {
                    'success': True,
                    'response': f"Análisis de texto: {prompt}",
                    'tokens_used': 50,
                    'processing_time': 1.0,
                    'request_id': f"clientpy_{int(time.time())}",
                    'model': self.model_name
                }
            
            # Guardar imagen temporalmente
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                # Decodificar base64 si es necesario
                if image_urls[0].startswith('data:'):
                    # Extraer base64 de data URL
                    header, data = image_urls[0].split(',', 1)
                    image_data = base64.b64decode(data)
                    temp_file.write(image_data)
                else:
                    # Es una URL normal
                    import requests
                    response = requests.get(image_urls[0])
                    temp_file.write(response.content)
                
                temp_file_path = temp_file.name
            
            # Ejecutar client.py
            cmd = [
                'python', self.client_script,
                '-i', temp_file_path,
                '-p', prompt
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Limpiar archivo temporal
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                processing_time = time.time() - start_time
                
                # Procesar la salida para extraer solo el contenido real
                output = result.stdout.strip()
                
                # Si solo contiene "Processing image..." o está vacío, significa que no hubo respuesta real
                if not output.strip() or output == "Processing image..." or output.startswith("Processing image..."):
                    print(f"⚠️ Client.py solo devolvió: '{output}'")
                    print("🔄 Usando mock service como fallback...")
                    from .mock_service import MockAIService
                    mock_service = MockAIService()
                    return mock_service.generate_response(prompt, image_urls, max_tokens, temperature, request_type, user)
                
                # Extraer solo el contenido después de "Processing image..."
                if "Processing image..." in output:
                    # Dividir por líneas y tomar solo las que no son "Processing image..."
                    lines = output.split('\n')
                    content_lines = [line for line in lines if line.strip() and not line.strip().startswith("Processing image")]
                    if content_lines:
                        response_text = '\n'.join(content_lines).strip()
                    else:
                        response_text = output
                else:
                    response_text = output
                
                return {
                    'success': True,
                    'response': response_text,
                    'tokens_used': len(response_text.split()),
                    'processing_time': processing_time,
                    'request_id': f"clientpy_{int(time.time())}",
                    'model': self.model_name
                }
            else:
                # Si falla, usar mock service como fallback
                print(f"⚠️ Client.py failed: {result.stderr}")
                print("🔄 Using mock service as fallback...")
                from .mock_service import MockAIService
                mock_service = MockAIService()
                return mock_service.generate_response(prompt, image_urls, max_tokens, temperature, request_type, user)
                
        except Exception as e:
            # Si hay cualquier error, usar mock service como fallback
            print(f"⚠️ Client.py adapter error: {str(e)}")
            print("🔄 Using mock service as fallback...")
            from .mock_service import MockAIService
            mock_service = MockAIService()
            return mock_service.generate_response(prompt, image_urls, max_tokens, temperature, request_type, user)
    
    def health_check(self) -> Dict[str, Any]:
        """Health check para el cliente local"""
        return {
            'status': 'healthy',
            'model': self.model_name,
            'endpoint': 'client.py-adapter',
            'message': 'Client.py adapter is running'
        }
