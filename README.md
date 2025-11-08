# Crowd Counter

## Overview

This is a web-based crowd counting application that uses a deep learning model ( Convolutional Neural Network for Crowd Counting ) to analyze images and estimate crowd density. The application provides a user-friendly interface for uploading images, processing them through an AI model, and displaying results with visual heatmaps showing crowd distribution patterns.

![Crowd Counter Demo1]<img width="1920" height="902" alt="1" src="https://github.com/user-attachments/assets/5b68f529-4bc0-4c2e-b408-1c542a47278e" />

![Crowd Counter Demo2]<img width="1920" height="892" alt="2" src="https://github.com/user-attachments/assets/18bb90da-9603-4c38-8e48-a0d0fb974f8a" />

![Crowd Counter Demo3]<img width="1920" height="896" alt="3" src="https://github.com/user-attachments/assets/7b1514a7-0ff5-4b9f-90af-17b2b20be6ee" />

![Crowd Counter Demo4]<img width="1920" height="896" alt="4" src="https://github.com/user-attachments/assets/3483c081-d4d9-4368-82be-686aada6ad7e" />


![Crowd Counter Demo5]<img width="1920" height="896" alt="5" src="https://github.com/user-attachments/assets/2e198a98-6ba5-4e88-ac22-7421822678c3" />


![Crowd Counter Demo6]<img width="1920" height="896" alt="6" src="https://github.com/user-attachments/assets/8a49e0e5-9a1f-41a6-a40f-32db18599810" />


![Crowd Counter Demo7]<img width="1920" height="900" alt="7" src="https://github.com/user-attachments/assets/7eaf5f80-7abb-48ec-af97-1b30f81bb3f4" />


The system is built as a Flask web application that handles image uploads, processes them through a pre-trained neural network model, and returns both numerical crowd counts and visual density heatmaps. It supports common image formats and includes proper error handling for production deployment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

- **Template Engine**: Jinja2 templates with Bootstrap for responsive UI design
- **Styling**: Custom CSS with Bootstrap dark theme integration and Font Awesome icons
- **Interactive Features**: JavaScript-powered drag-and-drop file upload with live preview
- **User Experience**: Clean interface with progress indicators and flash message system

### Backend Architecture

- **Web Framework**: Flask application with ProxyFix middleware for production deployment
- **File Handling**: Secure file upload system with extension validation and size limits (16MB max)
- **Model Integration**: Lazy-loaded neural network model with global caching for performance
- **Image Processing**: PIL/OpenCV for image preprocessing and normalization
- **Visualization**: Matplotlib for generating crowd density heatmaps

### AI Model Integration

- **Model Format**: Keras/TensorFlow model stored as JSON architecture + HDF5 weights
- **Preprocessing Pipeline**: Image normalization with ImageNet statistics for RGB channels
- **Prediction Output**: Density maps converted to crowd counts and visual heatmaps
- **Fallback System**: Mock predictions when ML dependencies are unavailable

### Data Flow

- **Upload Pipeline**: File validation → secure storage → image preprocessing → model prediction
- **Result Generation**: Crowd count calculation + heatmap visualization + base64 encoding
- **Response Handling**: Template rendering with results or error feedback

### Configuration Management

- **Environment Variables**: Session secrets and configuration parameters
- **Directory Structure**: Organized folders for uploads, models, weights, and results
- **File Security**: Werkzeug secure filename handling and extension whitelisting

## External Dependencies

### Core Web Framework

- **Flask**: Web application framework with template rendering and routing
- **Werkzeug**: WSGI utilities for secure file handling and proxy support

### Machine Learning Stack

- **Keras/TensorFlow**: Neural network model loading and inference
- **NumPy**: Numerical computations and array operations
- **PIL (Pillow)**: Image loading and preprocessing
- **OpenCV**: Computer vision operations (cv2)
- **H5PY**: HDF5 file format support for model weights

### Visualization and UI

- **Matplotlib**: Heatmap generation and plot creation
- **Bootstrap**: Frontend CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements

### Development and Deployment

- **Python Standard Library**: OS operations, logging, base64 encoding, IO operations
- **WSGI Server**: Compatible with standard Python web servers for deployment

The application is designed to work with or without the ML dependencies, providing graceful degradation when the model files or libraries are unavailable.
