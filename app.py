import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Creamos una carpeta llamada 'mis_archivos_nube' en tu PC
UPLOAD_FOLDER = 'mis_archivos_nube'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subir-a-pc', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return "No se seleccionó nada", 400
    
    file = request.files['archivo']
    if file.filename == '':
        return "Nombre de archivo vacío", 400

    # Guardamos el archivo con su nombre original de forma segura
    filename = secure_filename(file.filename)
    path_final = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path_final)
    
    # Devolvemos el link para que lo vean en la web
    return f"http://127.0.0.1:5000/descargar/{filename}"

@app.route('/descargar/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)000)