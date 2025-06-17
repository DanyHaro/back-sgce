from flask import Blueprint, jsonify
from ...models import Resumen, db

# Crear el blueprint para los resúmenes
main_routes = Blueprint('resumenes', __name__)

# Ruta para obtener todos los resúmenes
@main_routes.route('/resumen', methods=['GET'])
def get_all_resumenes():
    resumenes = Resumen.query.all()  # Obtiene todos los resúmenes
    resumenes_list = []

    for resumen in resumenes:
        resumenes_list.append({
            'id': resumen.id,
            'id_sesion': resumen.id_sesion,
            'resumen_general': resumen.resumen_general,
            'proposito_clase': resumen.proposito_clase,
            'inicio': resumen.inicio,
            'desarrollo': resumen.desarrollo,
            'cierre': resumen.cierre
        })
    
    return jsonify(resumenes_list), 200

# Ruta para obtener un resumen por ID
@main_routes.route('/resumen/<int:id>', methods=['GET'])
def get_resumen_by_id(id):
    resumen = Resumen.query.get(id)  # Obtiene el resumen por ID
    if resumen:
        return jsonify({
            'id': resumen.id,
            'id_sesion': resumen.id_sesion,
            'resumen_general': resumen.resumen_general,
            'proposito_clase': resumen.proposito_clase,
            'inicio': resumen.inicio,
            'desarrollo': resumen.desarrollo,
            'cierre': resumen.cierre
        }), 200
    else:
        return jsonify({'message': 'Resumen no encontrado'}), 404

# Ruta para obtener los resúmenes por ID de sesión
@main_routes.route('/resumen/by-sesion/<int:id_sesion>', methods=['GET'])
def get_resumenes_by_sesion(id_sesion):
    resumenes = Resumen.query.filter_by(id_sesion=id_sesion).all()  # Filtra los resúmenes por ID de sesión
    if resumenes:
        resumenes_list = []
        for resumen in resumenes:
            resumenes_list.append({
                'id': resumen.id,
                'id_sesion': resumen.id_sesion,
                'resumen_general': resumen.resumen_general,
                'proposito_clase': resumen.proposito_clase,
                'inicio': resumen.inicio,
                'desarrollo': resumen.desarrollo,
                'cierre': resumen.cierre
            })
        return jsonify(resumenes_list), 200
    else:
        return jsonify({'message': 'No se encontraron resúmenes para esta sesión'}), 404
