from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Nombre del archivo Excel que actuará como base de datos
EXCEL_FILE = 'citas_nails.xlsx'

def guardar_en_excel(nueva_cita):
    # Si el archivo ya existe, lo abrimos; si no, creamos uno nuevo
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=['Fecha_Registro', 'Cliente', 'Fecha_Cita', 'Hora', 'Servicio'])

    # Agregamos la nueva fila
    nuevo_df = pd.DataFrame([nueva_cita])
    df = pd.concat([df, nuevo_df], ignore_index=True)

    # Guardamos el archivo en el servidor
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    try:
        datos = request.json
        cita = {
            'Fecha_Registro': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'Cliente': datos.get('cliente', 'Desconocido'),
            'Fecha_Cita': datos.get('fecha'),
            'Hora': datos.get('hora'),
            'Servicio': datos.get('servicio', 'Manicura')
        }
        
        guardar_en_excel(cita)
        return jsonify({"status": "success", "message": "¡Cita guardada en el Excel!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# RUTA SECRETA PARA LA DUEÑA
@app.route('/descargar-reporte')
def descargar_reporte():
    if os.path.exists(EXCEL_FILE):
        # Esto le envía el archivo Excel directamente al celular/PC
        return send_file(EXCEL_FILE, as_attachment=True)
    return "Todavía no hay citas registradas.", 404
