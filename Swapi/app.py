from flask import Flask, render_template,redirect,request,session,url_for,jsonify
from urllib.request import urlopen
import json

# SWAPI
url= "https://swapi.dev/api/"

def getapi(url,req):
    final_url=url+req
    json_obj=urlopen(final_url)
    data= json.load(json_obj)
    return data

def get_arid(url,req):
    data=getapi(url,req)
    film_group=[]
    for data_set in data["results"]:
        if data_set["climate"]=="arid":
            for film in data_set["films"]:
                if film not in film_group:
                    film_group.append("film")
    return len(film_group)

def get_starships(url,req):
    data=getapi(url,req)
    main=0
    name=""
    for data_set in data["results"]:
        capacity=int(data_set["cargo_capacity"])
        if capacity>main:
            main=capacity
            name=data_set["name"]
    return (name,main)

app=Flask(__name__)
app.config["SECRET_KEY"]="mysupersecret"

@app.route("/", methods=["GET","POST"])
def index():
    
    if request.method=="POST" and request.form["query"]=="":
        session.clear()
        return redirect(url_for("index"))
    
    if request.method=="POST":
        query= request.form["query"]
        data_object=getapi(url,query)
        session["object"]=data_object
        session["name"]=data_object["name"]
        return redirect(url_for("index"))

    arid=get_arid(url,"planets")
    starship=get_starships(url,"starships")
    return render_template("index.html",arid=arid,starship=starship)

if __name__ == "__main__":
    app.run(debug=True)