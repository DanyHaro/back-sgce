from flask import Blueprint, jsonify, request
from ...models import Resumen, db,Sesion

# Crear el blueprint para los resúmenes
main_routes = Blueprint('resumenes', __name__)

@main_routes.route('/resumen/create', methods=['POST'])
def create_resumen():
    data = request.get_json()

    # Validación básica del campo obligatorio
    id_sesion = data.get('id_sesion')
    if not id_sesion:
        return jsonify({'error': 'id_sesion es obligatorio'}), 400

    # Verificar que la sesión exista
    sesion = Sesion.query.filter_by(id=id_sesion).first()
    if not sesion:
        return jsonify({'error': 'Sesión no encontrada'}), 404

    # Crear instancia del resumen
    nuevo_resumen = Resumen(
        id_sesion=id_sesion,
        resumen_general=data.get('resumen_general'),
        proposito_clase=data.get('proposito_clase'),
        inicio=data.get('inicio'),
        desarrollo=data.get('desarrollo'),
        cierre=data.get('cierre')
    )

    db.session.add(nuevo_resumen)
    db.session.commit()

    return jsonify({
        'message': 'Resumen creado exitosamente',
        'resumen': {
            'id': nuevo_resumen.id,
            'id_sesion': nuevo_resumen.id_sesion,
            'resumen_general': nuevo_resumen.resumen_general,
            'proposito_clase': nuevo_resumen.proposito_clase,
            'inicio': nuevo_resumen.inicio,
            'desarrollo': nuevo_resumen.desarrollo,
            'cierre': nuevo_resumen.cierre
        }
    }), 201



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
