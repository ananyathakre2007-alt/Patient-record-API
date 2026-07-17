from fastapi import FastAPI,Path, HTTPException,Query
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
def view_patient(patient_id : str=Path(...,description='id of the patient in DB',example='P001')):
     
    #load all patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    
    
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by : str= Query(...,description='sort patients on the basis of height,weight or bmi'),order:str=Query('asc',description='Arrange in asc or desc order')):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid request... select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException (status_code=400,detail='Invalid request ... select asc or desc')

    data=load_data()
    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0),reversed=sort_order)

    return sorted_data

    