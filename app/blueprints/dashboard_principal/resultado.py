from flask import Blueprint, jsonify, request
from ...models import ResultadoRubrica, db,Sesion, Rubrica

main_routes = Blueprint('resultados_rubrica', __name__)

@main_routes.route('/rubrica', methods=['GET'])
def list_rubricas():
    rubricas = Rubrica.query.all()

    resultado = []
    for r in rubricas:
        resultado.append({
            'id': r.id,
            'factores': r.factores,
            'criterios': r.criterios,
            'items': r.items
        })

    return jsonify({'rubricas': resultado}), 200

