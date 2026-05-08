from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Archivo donde se guardarán las citas
DATA_FILE = 'citas.json'


def cargar_citas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def guardar_cita(nueva_cita):
    citas = cargar_citas()
    citas.append(nueva_cita)
    with open(DATA_FILE, 'w') as f:
        json.dump(citas, f, indent=4)

        @app.route('/')
        def home():
            return render_template('index.html')


@app.route('/agendar', methods=['POST'])
def agendar():
    datos = request.json
    fecha = datos['fecha']
    hora = datos['hora']  # Ejemplo: "02:30 PM"

    citas = cargar_citas()

    # VALIDACIÓN: ¿Ya existe una cita en esa fecha y hora?
    for cita in citas:
        if cita['fecha'] == fecha and cita['hora'] == hora:
            return jsonify(
                {"status": "error", "message": "¡Lo siento! Esta hora ya está ocupada. Por favor elige otra."}), 400

    # Si está libre, guardamos
    guardar_cita(datos)
    return jsonify({"status": "success", "message": "Cita agendada correctamente."})


if __name__ == '__main__':
    app.run(debug=True)
