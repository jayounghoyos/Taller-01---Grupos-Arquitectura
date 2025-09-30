from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services import ProductAIService
from .factory import create_ai_client




@swagger_auto_schema(
    method='get',
    operation_description="Verifica el estado del servicio de IA",
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Verifica el estado del servicio de IA
    """
    try:
        ai_client = create_ai_client()
        ai_service = ProductAIService(ai_client=ai_client)
        health_status = ai_service.health_check()
        
        if health_status['status'] == 'healthy':
            return Response(health_status, status=status.HTTP_200_OK)
        else:
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
    except Exception as e:
        
        return Response(
            {'status': 'unhealthy', 'error': str(e)}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@swagger_auto_schema(
    method='post',
    operation_description="Analiza una imagen de producto subida directamente y genera información completa",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE, description='Archivo de imagen del producto'),
        },
        required=['image']
    ),
)
@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_product_image_upload(request):
    """
    Analiza una imagen de producto subida directamente y genera información completa para auto-llenar formulario
    """
    try:
        image_file = request.FILES.get('image')
        
        if not image_file:
            return Response(
                {'error': 'No se proporcionó imagen'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convertir imagen a base64 para enviar directamente
        import base64
        from PIL import Image
        import io
        
        # Leer y redimensionar la imagen para reducir el tamaño
        image_content = image_file.read()
        
        # Abrir imagen con PIL
        image = Image.open(io.BytesIO(image_content))
        
        # Redimensionar si es muy grande (máximo 800x600)
        if image.width > 800 or image.height > 600:
            image.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Convertir a JPEG para reducir tamaño
        output = io.BytesIO()
        image.convert('RGB').save(output, format='JPEG', quality=85)
        image_content = output.getvalue()
        
        # Convertir a base64
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        
        # Crear URL de datos (data URL)
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        
        
        
        # Realizar análisis completo - usar el adaptador que funciona
        ai_client = create_ai_client(provider='clientpy')
        ai_service = ProductAIService(ai_client=ai_client)
        result = ai_service.analyze_product_complete(image_url, user=request.user)
        
        if result['success']:
            return Response({
                'success': True,
                'data': result['data'],
                'request_id': result.get('request_id'),
                'processing_time': result.get('processing_time')
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'Error en el análisis de IA'),
                'raw_response': result.get('raw_response')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )