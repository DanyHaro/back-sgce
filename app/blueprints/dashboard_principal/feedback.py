from flask import Blueprint, jsonify, request
from ...models import Feedback, db,Sesion

main_routes = Blueprint('retroalimentacion', __name__)

from datetime import datetime

@main_routes.route('/feedback/create', methods=['POST'])
def create_feedback():
    data = request.get_json()

    # Validación del campo obligatorio
    id_sesion = data.get('id_sesion')
    if not id_sesion:
        return jsonify({'error': 'id_sesion es obligatorio'}), 400

    # Verificar si la sesión existe
    sesion = Sesion.query.filter_by(id=id_sesion).first()
    if not sesion:
        return jsonify({'error': 'Sesión no encontrada'}), 404

    # Asignar fecha actual automáticamente
    fecha_feedback = datetime.now().strftime('%Y-%m-%d')

    # Crear instancia de Feedback
    nuevo_feedback = Feedback(
        observacion=data.get('observacion', ''),
        hallazgos=data.get('hallazgos', ''),
        recomendacion=data.get('recomendacion', ''),
        fecha_feedback=fecha_feedback,
        id_sesion=id_sesion
    )

    db.session.add(nuevo_feedback)
    db.session.commit()

    return jsonify({
        'message': 'Feedback creado exitosamente',
        'feedback': {
            'id': nuevo_feedback.id,
            'observacion': nuevo_feedback.observacion,
            'hallazgos': nuevo_feedback.hallazgos,
            'recomendacion': nuevo_feedback.recomendacion,
            'fecha_feedback': nuevo_feedback.fecha_feedback.strftime('%Y-%m-%d'),
            'id_sesion': nuevo_feedback.id_sesion
        }
    }), 201












