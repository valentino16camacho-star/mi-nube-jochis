import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta de tu nube personal
CARPETA = 'mis_archivos_nube'
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

app.config['UPLOAD_FOLDER'] = CARPETA

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subir', methods=['POST'])
def subir():
    if 'archivo' not in request.files:
        return 'No hay archivo', 400
    f = request.files['archivo']
    if f.filename == '':
        return 'Sin nombre', 400
    
    nombre = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre))
    return 'OK'

@app.route('/lista-archivos')
def lista_archivos():
    # Lee todos los archivos de la carpeta
    archivos = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(archivos)

@app.route('/descargar/<nombre>')
def descargar(nombre):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nombre)

if __name__ == '__main__':
    app.run(debug=True, port=5000)