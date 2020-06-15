import os

from flask import Flask,url_for,redirect,render_template,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import AddSlang, DelSlang

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
db=SQLAlchemy(app)

app.config["SECRET_KEY"]=os.environ["dbpass"]
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

Migrate(app,db)

#Model

class Slang(db.Model):

    __tablename__="slangs"

    id=db.Column(db.Integer, primary_key=True)
    palabra=db.Column(db.String)
    definicion=db.Column(db.String)

    def __init__(self, palabra,definicion):
        self.palabra=palabra
        self.definicion=definicion
    
    def __repr__(self):
        return f"En Panama {self.palabra}  significa {self.definicion}"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET","POST"])
def add():
    
    form=AddSlang()

    if form.validate_on_submit():
        flash("Slang Añadido Exitosamente")
        palabra=form.palabra.data
        definicion=form.definicion.data
        slang=Slang(palabra,definicion)
        db.session.add(slang)
        db.session.commit()

        return redirect(url_for("lista"))

    return render_template("add.html", form=form)

@app.route("/delete", methods=["GET","POST"])
def delete():
    
    form=DelSlang()

    if form.validate_on_submit():
        flash("Slang Eliminado Exitosamente")
        palabra=form.palabra.data
        palabra_eliminada=Slang.query.filter_by(palabra=palabra).first()
        db.session.delete(palabra_eliminada)
        db.session.commit()

        return redirect(url_for("lista"))

    return render_template("delete.html", form=form)

@app.route("/list")
def lista():
    slangs=Slang.query.all()
    return render_template("lista.html", slangs=slangs)

if __name__ == "__main__":
    app.run(debug=True)
