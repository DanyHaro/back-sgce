from flask import Blueprint, jsonify, request
from ...models import ResultadoRubrica, db,Sesion, Rubrica

main_routes = Blueprint('resultados_rubrica', __name__)

@main_routes.route('/rubrica', methods=['GET'])
def get_rubricas():
    rubricas = Rubrica.query.all()
    factores = []
    
    # Agrupamos los resultados por factores
    for rubrica in rubricas:
        factor_exist = next((factor for factor in factores if factor['nombre'] == rubrica.factores), None)
        
        if not factor_exist:
            factor_exist = {
                'nombre': rubrica.factores,
                'criterios': []
            }
            factores.append(factor_exist)
        
        # Agregar los criterios dentro del factor
        criterio = {
            'nombre': rubrica.criterios,
            'itemsEvaluacion': []
        }
        
        # Desglosar los items
        items = rubrica.items.split('\n')
        for i, item in enumerate(items, start=1):
            criterio['itemsEvaluacion'].append({
                'id': i,
                'nombre': item.strip()
            })
        
        factor_exist['criterios'].append(criterio)

    return jsonify({"factores": factores})