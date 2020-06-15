from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

class AddSlang(FlaskForm):

    palabra=StringField("Inserte la palabra que desea agregar", validators=[DataRequired()])
    definicion=StringField("Inserte la definicion de la palabra", validators=[DataRequired()])
    submit=SubmitField()
    
class DelSlang(FlaskForm):

    palabra=StringField("Inserte la palabra que desea eliminar", validators=[DataRequired()])
    submit=SubmitField()