from flask import Flask, jsonify, request
import json
import yaml
from dicttoxml import dicttoxml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_FOLDER = os.path.join(BASE_DIR, "DOCENTES")
if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

app = Flask(__name__)

# --- Base de datos temporal en memoria ---
docentes = []

@app.route("/")
def home():
    return "API de Registro de Docentes"

# --- Registrar docente ---
@app.route("/profes", methods=["GET", "POST"])
def registrar_docente():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form  

        docente = {
            "nombre": data.get("nombre"),
            "num_empleado": data.get("num_empleado"),
            "carrera": data.get("carrera")
        }
        docentes.append(docente)
        return jsonify({"mensaje": "Docente registrado", "total": len(docentes)}), 201
    else:
        # muestra un formulario sencillo
        return '''
        <h2>Registrar Docente</h2>
        <form method="POST" action="/profes">
            Nombre: <input type="text" name="nombre"><br>
            Número de empleado: <input type="text" name="num_empleado"><br>
            Carrera: <input type="text" name="carrera"><br>
            <button type="submit">Registrar</button>
        </form>
        '''
        


# --- Listar todos los docentes ---
@app.route("/docentes", methods=["GET", "POST"])
def listar_docentes():
    return jsonify(docentes), 200

    

# --- Exportar JSON ---
@app.route("/exportar/json", methods=["GET"])
def exportar_json():
    file_path = os.path.join(EXPORT_FOLDER, "docentes.json")
    with open("docentes.json", "w", encoding="utf-8") as f:
        json.dump(docentes, f, ensure_ascii=False, indent=4)
    return jsonify({"mensaje": "Archivo docentes.json generado correctamente"}), 200

# --- Exportar YAML ---
@app.route("/exportar/yaml", methods=["GET"])
def exportar_yaml():
    file_path = os.path.join(EXPORT_FOLDER, "docentes.yaml")
    with open("docentes.yaml", "w", encoding="utf-8") as f:
        yaml.dump(docentes, f, allow_unicode=True)
    return jsonify({"mensaje": "Archivo docentes.yaml generado correctamente"}), 200

# --- Exportar XML ---
@app.route("/exportar/xml", methods=["GET"])
def exportar_xml():
    file_path = os.path.join(EXPORT_FOLDER, "docentes.xml")
    xml_data = dicttoxml(docentes, custom_root="docentes", attr_type=False)
    with open("docentes.xml", "wb") as f:
        f.write(xml_data)
    return jsonify({"mensaje": "Archivo docentes.xml generado correctamente"}), 200

if __name__ == "__main__":
    app.run(debug=True)