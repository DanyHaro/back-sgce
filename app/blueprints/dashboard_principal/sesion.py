from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage
import os
from datetime import datetime
from ...models import Sesion, db
from ...models import Transcripcion, Resumen, ResultadoRubrica, Feedback, User, db

main_routes = Blueprint('sesions', __name__)

# Configurar Firebase Admin SDK
cred = credentials.Certificate(r"C:\exam3-24564-firebase-adminsdk-uw7lf-beddd73802.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'exam3-24564.appspot.com' 
})

# Ruta para crear una nueva sesión con video MP4
@main_routes.route('/sesion/create-firebase', methods=['POST'])
def create_sesion_firebase():
    # Verificar si se ha enviado un archivo
    if 'grabacion' not in request.files:
        return jsonify({'message': 'Debe subir la grabación de la sesión.'}), 400

    video_file = request.files['grabacion']

    # Verificar si el archivo tiene un nombre
    if video_file.filename == '':
        return jsonify({'message': 'Debe subir la grabación de la sesión.'}), 400

    # Verificar si el archivo es un MP4
    if video_file and allowed_file(video_file.filename):
        # Crear un nombre seguro para el archivo
        filename = secure_filename(video_file.filename)

        # Subir el archivo a Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f"videos/{filename}")
        blob.upload_from_file(video_file)

        # Crear una URL pública del video almacenado
        video_url = blob.public_url

        # Crear un nuevo registro de sesión en la base de datos
        new_sesion = Sesion(
            titulo=request.form.get('titulo'),
            institucion=request.form.get('institucion'),
            fecha_dictada=request.form.get('fecha_dictada'),
            duracion_video=request.form.get('duracion_video'),
            descripcion = request.form.get('descripcion'),
            fecha_creacion=datetime.now().strftime('%Y-%m-%d'),
            grabacion=video_url,
            auditado=False,
            id_user=request.form.get('id_user')
        )

        # Guardar la sesión en la base de datos
        db.session.add(new_sesion)
        db.session.commit()

        return jsonify({'message': 'Sesión creada con éxito'}), 201
    else:
        return jsonify({'message': 'El archivo debe ser un MP4'}), 400


# Ruta para crear una nueva sesión con video
@main_routes.route('/sesion/create', methods=['POST'])
def create_sesion():
    # Verificar si se ha enviado un archivo
    if 'grabacion' not in request.files:
        return jsonify({'message': 'Debe subir la grabación de la sesión.'}), 400

    video_file = request.files['grabacion']

    # Verificar si el archivo tiene un nombre
    if video_file.filename == '':
        return jsonify({'message': 'Debe subir la grabación de la sesión.'}), 400

    # Verificar si el archivo es un MP4
    if video_file and allowed_file(video_file.filename):
        # Crear un nombre seguro para el archivo
        filename = secure_filename(video_file.filename)

        # Guardar el archivo en la carpeta C:\sesiones
        upload_folder = r'C:\sesiones'
        video_file.save(os.path.join(upload_folder, filename))

        # Crear un nuevo registro de sesión en la base de datos
        new_sesion = Sesion(
            titulo=request.form.get('titulo'),
            institucion=request.form.get('institucion'),
            fecha_dictada=request.form.get('fecha_dictada'),
            duracion_video=request.form.get('duracion_video'),
            descripcion = request.form.get('descripcion'),
            fecha_creacion=datetime.now().strftime('%Y-%m-%d'),
            grabacion=filename,  # Guardar solo el nombre del archivo
            auditado=False,
            id_user=request.form.get('id_user')
        )

        # Guardar la sesión en la base de datos
        db.session.add(new_sesion)
        db.session.commit()

        return jsonify({'message': 'Sesión creada con éxito'}), 201
    else:
        return jsonify({'message': 'El archivo debe ser un MP4'}), 400

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

@main_routes.route('/sesion/get-details/<int:id_sesion>', methods=['GET'])
def get_sesion_details(id_sesion):

    sesion = Sesion.query.filter_by(id = id_sesion).first()
    user = User.query.filter_by(id = sesion.id_user).first()
    transcripcion = Transcripcion.query.filter_by(id_sesion=id_sesion).first()
    resumen = Resumen.query.filter_by(id_sesion=id_sesion).first()
    resultado_rubrica = ResultadoRubrica.query.filter_by(id_sesion=id_sesion).first()
    feedback = Feedback.query.filter_by(id_sesion=id_sesion).first()

    #if not transcripcion or not resumen or not resultado_rubrica or not feedback:
    #    return jsonify({'message': 'Datos no encontrados para la sesión especificada'}), 404

    # Crear la respuesta con los datos solicitados
    sesion_details = {
        'titulo': sesion.titulo,
        'institucion': sesion.institucion,
        'fecha_dictada': sesion.fecha_dictada,
        'duracion_video': sesion.duracion_video,
        'grabacion' : sesion.grabacion,
        'auditado' : sesion.auditado,
        'user': {
            'id': user.id,
            'nombre_completo': user.nombre_completo,
            'username': user.username,
            'email': user.email
        },
        'transcripcion': {
            'id': transcripcion.id,
            'palabras_clave': transcripcion.palabras_clave,
            'descripcion': transcripcion.descripcion
        },
        'resumen': {
            'id': resumen.id,
            'resumen_general': resumen.resumen_general,
            'proposito_clase': resumen.proposito_clase,
            'inicio': resumen.inicio,
            'desarrollo': resumen.desarrollo,
            'cierre': resumen.cierre
        },
        'resultado_rubrica': {
            'id': resultado_rubrica.id,
            'cumple_satis': resultado_rubrica.cumple_satis,
            'cumple': resultado_rubrica.cumple,
            'cumple_parcial': resultado_rubrica.cumple_parcial,
            'cumple_no': resultado_rubrica.cumple_no
        },
        'feedback': {
            'id': feedback.id,
            'observacion': feedback.observacion,
            'hallazgos': feedback.hallazgos,
            'recomendacion': feedback.recomendacion,
            'fecha_feedback': feedback.fecha_feedback.strftime('%Y-%m-%d')  # Formateamos la fecha
        }
    }

    return jsonify(sesion_details), 200


# Función para verificar si el archivo es MP4
def allowed_file(filename):
    allowed_extensions = {'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions