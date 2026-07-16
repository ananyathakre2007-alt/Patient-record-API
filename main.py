from fastapi import FastAPI
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

#home route
@app.get("/")
def home():
    return{"message":"Patient Management system API"}

#about  route
@app.get("/about")
def about():
    return{"message":"A Fully Functional API to manage your patients records"}

#view route
@app.get("/view")
def view():
    data=load_data()

    return data
