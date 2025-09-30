import argparse
from openai import OpenAI
from termcolor import colored

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
                            "url": image_path,
                        },
                    },
                ],
            }
        ],
        stream=True,
        max_tokens=256,
    )

    # Process streaming response
    print(colored("Processing image...", "yellow"))
    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        print(colored(content, "green"), end="", flush=True)

    print()  # New line at the end

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
