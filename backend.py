from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 1. RUTA PRINCIPAL: Esta es la que abre tu index.html
@app.route('/')
def home():
    # Esto busca el archivo index.html dentro de la carpeta 'templates'
    return render_template('index.html')

# 2. RUTA PARA AGENDAR: La lógica que ya tenías
@app.route('/agendar', methods=['POST'])
def agendar():
    try:
        datos = request.json
        fecha = datos.get('fecha')
        hora = datos.get('hora')
        cliente = datos.get('cliente', 'Cliente Generico')
        
        # Aquí puedes agregar lógica para guardar en un JSON o base de datos
        print(f"Cita recibida: {cliente} para el {fecha} a las {hora}")
        
        return jsonify({"status": "success", "message": "Cita agendada correctamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# 3. CONFIGURACIÓN PARA RENDER
if __name__ == '__main__':
    # Esto solo se usa si corres el script localmente
    app.run(debug=True)
