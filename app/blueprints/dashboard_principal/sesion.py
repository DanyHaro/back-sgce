from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ...models import Sesion, db

main_routes = Blueprint('sesions', __name__)

@main_routes.route('/sesion', methods=['GET'])
def get_all_sessions():
    sesiones = Sesion.query.all()  # Obtiene todas las sesiones
    sesiones_list = []

    for sesion in sesiones:
        sesiones_list.append({
            'id': sesion.id,
            'titulo': sesion.titulo,
            'fecha_dictada': sesion.fecha_dictada.strftime('%Y-%m-%d'),  
            'duracion_video': str(sesion.duracion_video),  
            'fecha_creacion': sesion.fecha_creacion.strftime('%Y-%m-%d'),  
            'id_user': sesion.id_user
        })
    return jsonify(sesiones_list), 200

@main_routes.route('/sesion/<int:id>', methods=['GET'])
def get_session_by_id(id):
    sesion = Sesion.query.get(id)  # Obtiene la sesión por el ID
    if sesion:
        return jsonify({
            'id': sesion.id,
            'titulo': sesion.titulo,
            'fecha_dictada': sesion.fecha_dictada.strftime('%Y-%m-%d'),
            'duracion_video': str(sesion.duracion_video),
            'fecha_creacion': sesion.fecha_creacion.strftime('%Y-%m-%d'),
            'id_user': sesion.id_user
        }), 200
    else:
        return jsonify({'message': 'Sesión no encontrada'}), 404
