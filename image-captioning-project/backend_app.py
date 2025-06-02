from flask import Flask, request, jsonify, send_from_directory
import os
import sys
from werkzeug.utils import secure_filename

# Add the src directory to the Python path to allow importing generate_captions
# This assumes your Flask app (backend_app.py) is in the root of image-captioning-project
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'src'))

from inference.generate_captions import generate_caption_from_image_path, generate_caption_from_image_bytes
from config import DATA_DIR # To save uploaded images temporarily

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/caption', methods=['POST'])
def upload_and_caption_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(image_path)
            print(f"Image saved to {image_path}")
            
            # Generate caption using the path
            caption = generate_caption_from_image_path(image_path)
            
            # Clean up the uploaded image after captioning (optional)
            # os.remove(image_path)
            
            if "Error:" in caption:
                 return jsonify({"error": caption}), 500
            return jsonify({"caption": caption})
        except Exception as e:
            # os.remove(image_path) # Clean up if error occurs
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "Image Captioning API is running", "endpoints": ["/api/caption"]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT or default to 5000
    app.run(debug=False, host='0.0.0.0', port=port)  # Bind to all interfaces
