from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ],
    "proximo_id": 3
}

# Autenticación básica
def autenticacion_basica(usuario, contrasena):
    return usuario == 'admin' and contrasena == 'admin1'

# Ruta para obtener usuarios (no requiere autenticación)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para buscar un usuario por ID (no requiere autenticación)
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

# Ruta para agregar un nuevo usuario (requiere autenticación)
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    auth = request.authorization
    if not auth or not autenticacion_basica(auth.username, auth.password):
        return Response('No autorizado', 401, {'WWW-Authenticate': 'Basic realm="Login requerido"'})
    
    datos = request.json
    nombre = datos.get('nombre')
    
    # Validación de datos
    if not nombre or any(u["nombre"] == nombre for u in base_datos["usuarios"]):
        return jsonify({"mensaje": "Nombre inválido o usuario ya existe"}), 400
    
    nuevo_usuario = {
        "id": base_datos["proximo_id"],
        "nombre": nombre
    }
    
    base_datos["usuarios"].append(nuevo_usuario)
    base_datos["proximo_id"] += 1
    
    return jsonify(nuevo_usuario), 201

# Ruta para eliminar un usuario (requiere autenticación)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    auth = request.authorization
    if not auth or not autenticacion_basica(auth.username, auth.password):
        return Response('No autorizado', 401, {'WWW-Authenticate': 'Basic realm="Login requerido"'})
    
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)
    if usuario:
        base_datos["usuarios"].remove(usuario)
        return jsonify({"mensaje": "Usuario eliminado"}), 200
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000)
