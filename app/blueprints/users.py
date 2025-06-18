from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User, Role, db

main_routes = Blueprint('users', __name__)

# Ruta para crear un nuevo usuario
@main_routes.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud
    username = data.get('username')
    nombre_completo = data.get('nombre_completo')
    password = data.get('password')
    email = data.get('email')

    # Verificar que todos los campos necesarios estén presentes
    if not username or not password or not email:
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    # Crear un nuevo objeto User
    new_user = User(nombre_completo = nombre_completo,username=username, email=email)
    new_user.set_password(password)  # Usar el método set_password para encriptar la contraseña

    # Agregar el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente", "id": new_user.id}), 201


# Ruta para verificar la contraseña de un usuario
@main_routes.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud
    
    # Obtener el nombre de usuario o correo electrónico y la contraseña de la solicitud
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return jsonify({"message": "Inicio de sesión exitoso", "user_id": user.id, "status_code": 200}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas", "status_code": 401}), 401

@main_routes.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()  # Obtiene todos los usuarios
    users_list = []

    for user in users:
        users_list.append({
            'id': user.id,
            'nombre_completo': user.nombre_completo,
            'username': user.username,
            'email': user.email
        })
    
    return jsonify(users_list), 200

@main_routes.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)  # Obtiene el usuario por ID
    if user:
        return jsonify({
            'id': user.id,
            'nombre_completo': user.nombre_completo,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404