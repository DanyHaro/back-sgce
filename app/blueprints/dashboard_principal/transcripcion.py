from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ...models import Transcripcion, db

main_routes = Blueprint('transcripciones', __name__)

@main_routes.route('/trans', methods=['GET'])
def get_all_transcripciones():
    transcripciones = Transcripcion.query.all()  # Obtiene todas las transcripciones
    transcripciones_list = []

    for transcripcion in transcripciones:
        transcripciones_list.append({
            'id': transcripcion.id,
            'palabras_clave': transcripcion.palabras_clave,
            'descripcion': transcripcion.descripcion,
            'id_sesion': transcripcion.id_sesion
        })
    
    return jsonify(transcripciones_list), 200

@main_routes.route('/trans/<int:id>', methods=['GET'])
def get_transcripcion_by_id(id):
    transcripcion = Transcripcion.query.get(id)  # Obtiene la transcripción por ID
    if transcripcion:
        return jsonify({
            'id': transcripcion.id,
            'palabras_clave': transcripcion.palabras_clave,
            'descripcion': transcripcion.descripcion,
            'id_sesion': transcripcion.id_sesion
        }), 200
    else:
        return jsonify({'message': 'Transcripción no encontrada'}), 404


@main_routes.route('/trans/sesion/<int:id_sesion>', methods=['GET'])
def get_transcripciones_by_sesion(id_sesion):
    transcripciones = Transcripcion.query.filter_by(id_sesion=id_sesion).all()  # Filtra las transcripciones por ID de sesión
    if transcripciones:
        transcripciones_list = []
        for transcripcion in transcripciones:
            transcripciones_list.append({
                'id': transcripcion.id,
                'palabras_clave': transcripcion.palabras_clave,
                'descripcion': transcripcion.descripcion,
                'id_sesion': transcripcion.id_sesion
            })
        return jsonify(transcripciones_list), 200
    else:
        return jsonify({'message': 'No se encontraron transcripciones para esta sesión'}), 404
