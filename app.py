import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import base64
from io import BytesIO
from prediction import predict, load_model
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('weights', exist_ok=True)
os.makedirs('results', exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_heatmap_base64(heatmap_data):
    """Convert heatmap data to base64 encoded image string."""
    try:
        plt.figure(figsize=(10, 8))
        plt.imshow(heatmap_data.reshape(heatmap_data.shape[1], heatmap_data.shape[2]), 
                   cmap=cm.jet, interpolation='bilinear')
        plt.colorbar(label='Density')
        plt.title('Crowd Density Heat Map')
        plt.axis('off')
        
        # Save to BytesIO
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        
        return img_base64
    except Exception as e:
        logging.error(f"Error creating heatmap: {str(e)}")
        return None

def create_original_image_base64(image_data):
    """Convert original image data to base64 encoded string."""
    try:
        # Denormalize the image
        img = image_data.copy()
        img[:, :, 0] = (img[:, :, 0] * 0.229) + 0.485
        img[:, :, 1] = (img[:, :, 1] * 0.224) + 0.456
        img[:, :, 2] = (img[:, :, 2] * 0.225) + 0.406
        
        # Clip values to [0, 1] range
        img = np.clip(img, 0, 1)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(img.reshape(img.shape[1], img.shape[2], img.shape[3]))
        plt.title('Original Image')
        plt.axis('off')
        
        # Save to BytesIO
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        
        return img_base64
    except Exception as e:
        logging.error(f"Error creating original image: {str(e)}")
        return None

@app.route('/')
def index():
    """Main upload page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Check file type
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files only.', 'error')
            return redirect(request.url)
        
        if file and file.filename:
            # Secure the filename
            filename = secure_filename(file.filename or 'uploaded_image')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save uploaded file
            file.save(filepath)
            logging.info(f"File saved: {filepath}")
            
            # Make prediction
            try:
                count, image, heatmap = predict(filepath)
                logging.info(f"Prediction successful. Count: {count}")
                
                # Create base64 encoded images
                heatmap_base64 = create_heatmap_base64(heatmap)
                original_image_base64 = create_original_image_base64(image)
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass
                
                return render_template('result.html', 
                                     count=int(round(count)),
                                     original_image=original_image_base64,
                                     heatmap_image=heatmap_base64,
                                     filename=filename)
                
            except Exception as e:
                logging.error(f"Prediction error: {str(e)}")
                logging.error(traceback.format_exc())
                flash(f'Error processing image: {str(e)}', 'error')
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass
                
                return redirect(url_for('index'))
                
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        logging.error(traceback.format_exc())
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash("File is too large. Please upload a file smaller than 16MB.", 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    logging.error(f"Internal server error: {error}")
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
