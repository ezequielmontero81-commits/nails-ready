from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Nombre del archivo Excel que actuará como base de datos temporal
EXCEL_FILE = 'citas_nails.xlsx'

def guardar_en_excel(nueva_cita):
    """Función para registrar la cita en el archivo Excel"""
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        # Si no existe, creamos la estructura básica
        df = pd.DataFrame(columns=['Fecha_Registro', 'Cliente', 'Fecha_Cita', 'Hora', 'Servicio'])

    # Agregamos la nueva fila usando concat (método moderno de Pandas)
    nuevo_df = pd.DataFrame([nueva_cita])
    df = pd.concat([df, nuevo_df], ignore_index=True)

    # Guardamos el archivo físicamente en el servidor de Render
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    """Ruta principal que muestra tu página web"""
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    """Ruta que recibe los datos del formulario de la clienta"""
    try:
        datos = request.json
        if not datos:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400
            
        cita = {
            'Fecha_Registro': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'Cliente': datos.get('cliente', 'Desconocido'),
            'Fecha_Cita': datos.get('fecha'),
            'Hora': datos.get('hora'),
            'Servicio': datos.get('servicio', 'Manicura/Pedicura')
        }
        
        guardar_en_excel(cita)
        return jsonify({"status": "success", "message": "¡Cita guardada con éxito!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en el servidor: {str(e)}"}), 500

@app.route('/descargar-reporte')
def descargar_reporte():
    """Ruta para que la dueña baje el Excel acumulado"""
    if os.path.exists(EXCEL_FILE):
        # Envía el archivo para descarga automática
        return send_file(EXCEL_FILE, as_attachment=True)
    else:
        # Plan B: Si entras al link antes de que haya citas, verás este mensaje
        return """
        <h1>Aún no hay registros</h1>
        <p>El archivo de Excel se creará automáticamente cuando la primera clienta agende una cita.</p>
        <a href="/">Volver a la página principal para hacer una prueba</a>
        """, 200

if __name__ == '__main__':
    # Puerto dinámico para Render o local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
