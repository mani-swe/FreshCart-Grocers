import os
from flask import Flask, render_template, request, jsonify
from src.summariser import FreshCartSummariser

app = Flask(__name__)
summariser = FreshCartSummariser()

# Temp folder for uploaded files during web request
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request."})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected."})
    
    # Save file temporarily
    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_path)
    
    try:
        # Run through our validator & summariser logic
        result = summariser.generate_summary(temp_path)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify(result)
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)