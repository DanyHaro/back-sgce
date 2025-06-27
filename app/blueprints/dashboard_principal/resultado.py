from flask import Blueprint, jsonify, request
from ...models import ResultadoRubrica, db,Sesion, Rubrica

main_routes = Blueprint('resultados_rubrica', __name__)

@main_routes.route('/rubrica', methods=['GET'])
def get_rubricas():
    rubricas = Rubrica.query.all()
    factores = []

    # Agrupamos los resultados por factores
    for rubrica in rubricas:
        # Verificar si el factor ya está en la lista de factores
        factor_exist = next((factor for factor in factores if factor['nombre'] == rubrica.factores), None)

        if not factor_exist:
            # Si el factor no existe, lo agregamos
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
            # Agregar cada item al criterio con un id
            criterio['itemsEvaluacion'].append({
                'id': i,
                'nombre': item.strip()
            })

        # Agregar el criterio al factor correspondiente
        factor_exist['criterios'].append(criterio)

    # Devolvemos el resultado en el formato esperado
    return jsonify({"factores": factores})
