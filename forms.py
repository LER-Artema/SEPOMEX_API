from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class CpSearchForm(FlaskForm):
    cp = IntegerField('Código Postal', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class NameSearchForm(FlaskForm):
    name = StringField('Nombre de la entidad /municipio/ colonia ', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class AddForm(FlaskForm):
    cp_colonia = IntegerField('Código Postal', validators=[DataRequired()])
    nombre_colonia = StringField('Estado', validators=[DataRequired()])
    tipo_de_asentamiento = StringField('Tipo de asentamiento', validators=[DataRequired()])
    nombre_municipio = StringField('Nombre del municipio', validators=[DataRequired()])
    id_municipio = IntegerField('ID del municipio', validators=[DataRequired()])
    nombre_estado = StringField('Nombre del estado', validators=[DataRequired()])
    id_estado = IntegerField('ID del estado', validators=[DataRequired()])
    submit = SubmitField('Añadir')