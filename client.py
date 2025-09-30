import argparse
import sys
from openai import OpenAI

# Initialize the OpenAI client pointing to your Lightning endpoint
client = OpenAI(
    base_url="https://8001-01k4ap2fswtrsc3fyamsj261fp.cloudspaces.litng.ai/v1/",
    api_key="gemma3-litserve",  # no se valida, solo es placeholder
)

def send_request(image_path: str, prompt: str):
    """
    Sends a POST request to the server API endpoint with the given prompt and image.

    Args:
        - image_path (str): The path or URL to the input image.
        - prompt (str): The prompt to be sent in the request.
    """
    # Convertir archivo local a data URL si es necesario
    import base64
    
    if image_path.startswith('data:'):
        # Ya es una data URL
        image_url = image_path
    else:
        # Es un archivo local, convertir a data URL
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{image_base64}"
    
    # Send request to server
    response = client.chat.completions.create(
        model="google/gemma-3-4b-it",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        stream=True,
        max_tokens=256,
    )

    # Process streaming response - SIN colores para evitar problemas con subprocess
    full_response = ""
    try:
        for chunk in response:
            if hasattr(chunk, 'choices') and chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    full_response += delta.content
    except Exception as e:
        print(f"Error en streaming: {e}", file=sys.stderr)
        return
    
    # Imprimir solo la respuesta final, sin colores
    if full_response.strip():
        print(full_response)
    else:
        print("No se recibió respuesta del modelo", file=sys.stderr)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Send an image to the server to generate a caption."
    )
    parser.add_argument("-i", "--image", required=True, help="Path or URL to the input image")
    parser.add_argument(
        "-p",
        "--prompt",
        help="Prompt for the image",
        default="Describe this image in detail.",
    )
    args = parser.parse_args()

    # Call the function to send the request
    send_request(args.image, args.prompt)
