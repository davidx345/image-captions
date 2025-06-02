import os
import google.generativeai as genai
from PIL import Image
import io
from config import GEMINI_API_KEY, DATA_DIR # Assuming your API key and data directory are in config.py

# Configure the Gemini API key
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please set it in your .env file and ensure config.py loads it.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
# For image captioning, you'll typically use a model that supports multimodal inputs
# Check the Gemini documentation for the latest recommended model for image understanding, e.g., 'gemini-pro-vision'
try:
    # Using gemini-1.5-flash-latest to ensure the most up-to-date flash model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    # Updated error message to be more generic for model access issues
    print("Please ensure your API key is valid and has access to the specified Gemini model.")
    model = None # Set model to None if initialization fails

def generate_caption_from_image_path(image_path: str, prompt: str = "Describe this image in detail.") -> str:
    """
    Generates a caption for a local image using the Gemini API.

    Args:
        image_path (str): The local file path to the image.
        prompt (str): The prompt to guide the caption generation.

    Returns:
        str: The generated caption or an error message.
    """
    if not model:
        return "Gemini model not initialized. Please check API key and model access."

    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"

    try:
        print(f"Loading image from: {image_path}")
        img = Image.open(image_path)
        
        # The Gemini API for 'gemini-pro-vision' can often take PIL.Image objects directly
        # or image bytes. Let's try with the PIL Image object first.
        # The API expects a list of content parts.
        response = model.generate_content([prompt, img])
        
        # Ensure you are accessing the text part of the response correctly.
        # This might vary slightly based on the API version or response structure.
        # It's common for the response to have a 'text' attribute or a method like .text
        caption = response.text 
        return caption
    except FileNotFoundError:
        return f"Error: Image file not found at {image_path}"
    except Exception as e:
        return f"Error generating caption: {e}"

def generate_caption_from_image_bytes(image_bytes: bytes, prompt: str = "Describe this image in detail.") -> str:
    """
    Generates a caption for an image provided as bytes using the Gemini API.

    Args:
        image_bytes (bytes): The image data in bytes.
        prompt (str): The prompt to guide the caption generation.

    Returns:
        str: The generated caption or an error message.
    """
    if not model:
        return "Gemini model not initialized. Please check API key and model access."

    try:
        # Create a PIL Image object from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        response = model.generate_content([prompt, img])
        caption = response.text
        return caption
    except Exception as e:
        return f"Error generating caption from bytes: {e}"


if __name__ == "__main__":
    # This is an example of how to use the function.
    # Make sure you have an image in your DATA_DIR or provide a full path.
    # For example, if you have 'sample.jpg' in 'image-captioning-project/data/'
    
    sample_image_name = "sample.jpg" # Replace with your image file name
    image_path = os.path.join(DATA_DIR, sample_image_name)

    # Create a dummy sample image in DATA_DIR if it doesn't exist, for testing
    if not os.path.exists(image_path):
        try:
            print(f"Creating a dummy image at {image_path} for testing...")
            dummy_image = Image.new('RGB', (100, 100), color = 'red')
            dummy_image.save(image_path)
            print(f"Dummy image created. Please replace it with a real image to test captioning.")
        except Exception as e:
            print(f"Could not create dummy image: {e}")

    if os.path.exists(image_path) and model:
        print(f"Attempting to generate caption for: {image_path}")
        caption = generate_caption_from_image_path(image_path, prompt="What is in this picture?")
        print(f"\nGenerated Caption:\n{caption}")
    elif not model:
        print("Skipping caption generation example because the Gemini model could not be initialized.")
    else:
        print(f"Skipping caption generation example because the sample image '{image_path}' does not exist.")
        print("Please place an image there or update the 'sample_image_name'.")