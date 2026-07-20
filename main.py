from fastapi import FastAPI,Path, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional,Literal
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='id of the patient',example='P001')]
    name:Annotated[str,Field(...,description='name of the patient')]
    city:Annotated[str,Field(...,description='city of the patient ')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='age of the patient')]
    gender:Annotated[Literal['male','Male','Female','Others','female','others'],Field(...,description='gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient in meters')]
    weight:Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'



    
    


def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

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

    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0),reverse=sort_order)

    return sorted_data
    
@app.post('/create')
def create_patient(patient:Patient):
    #load data
    data=load_data()

    #check if patient exists
    if patient.id in data:
        raise HTTPException(400,detail='Patient already exists')
    
    #Add new patient to database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into json file
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'Pateint added successfully'})


    