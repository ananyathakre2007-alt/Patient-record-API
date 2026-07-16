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

#dynamic segment
@app.get("/patient/{patient_id}")
def view_patient(patient_id : str):
     
    #load all patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    
    else:
        return {"Error":"Patient not found"}
    

