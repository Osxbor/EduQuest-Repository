from flask import Blueprint, request, jsonify
from ..models.examenes import Examenes
from .. import db

ExamenesFiltros_bp = Blueprint('ExamenesFiltros_bp', __name__)

# Filtro por grado
@ExamenesFiltros_bp.route('/obtener/examenes/grado/<int:grado_id>', methods=['GET'])
def obtener_examenes_por_grado(grado_id):
    examenes = Examenes.query.filter_by(grado_id=grado_id).all()
    resultado = [examen.to_dict() for examen in examenes]
    return jsonify(resultado), 200

# Filtro por materia
@ExamenesFiltros_bp.route('/obtener/examenes/materia/<int:materia_id>', methods=['GET'])
def obtener_examenes_por_materia(materia_id):
    examenes = Examenes.query.filter_by(materia_id=materia_id).all()
    resultado = [examen.to_dict() for examen in examenes]
    return jsonify(resultado), 200

# Filtro por especialidad
@ExamenesFiltros_bp.route('/obtener/examenes/especialidad/<int:especialidad_id>', methods=['GET'])
def obtener_examenes_por_especialidad(especialidad_id):
    examenes = Examenes.query.filter_by(especialidad_id=especialidad_id).all()
    resultado = [examen.to_dict() for examen in examenes]
    return jsonify(resultado), 200

# Filtro por seccion
@ExamenesFiltros_bp.route('/obtener/examenes/seccion/<int:seccion_id>', methods=['GET'])
def obtener_examenes_por_seccion(seccion_id):
    examenes = Examenes.query.filter_by(seccion_id=seccion_id).all()
    resultado = [examen.to_dict() for examen in examenes]
    return jsonify(resultado), 200

# Filtro combinado
@ExamenesFiltros_bp.route('/obtener/examenes/filtrar', methods=['GET'])
def obtener_examenes_por_filtros():
    grado_id = request.args.get('grado_id', type=int)
    materia_id = request.args.get('materia_id', type=int)
    especialidad_id = request.args.get('especialidad_id', type=int)
    seccion_id = request.args.get('seccion_id', type=int)

    query = Examenes.query

    if grado_id is not None:
        query = query.filter_by(grado_id=grado_id)
    if materia_id is not None:
        query = query.filter_by(materia_id=materia_id)
    if especialidad_id is not None:
        query = query.filter_by(especialidad_id=especialidad_id)
    if seccion_id is not None:
        query = query.filter_by(seccion_id=seccion_id)

    examenes = query.all()
    result = [examen.to_dict() for examen in examenes]
    return jsonify(result), 200
