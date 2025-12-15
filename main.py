import json
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

app=FastAPI()


#Pydantic Object for type and value checking
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City of the patient')]
    age:Annotated[int, Field(...,gt=0,lt=120,description='Age of the Patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the Patient')]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


#Pydantic Object with optional variables to update the data
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


#helper functions
#Loading Data
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    
    return data 

#Saving the data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


#routes
@app.get("/")
def hello():
    return {'message':'Patient Management System API'}


@app.get('/about')
def about():
    return {'message':'A fully functional API to manage your patients records'}


#Viewing the entire data
@app.get('/view')
def view():
    data=load_data()
    return data


#Viewing the patients data with query parameters
@app.get('/patients/{patients_id}')
def view_patients(patients_id: str=Path(...,description='ID of the patient in the DB',example='P001')):
    data=load_data()

    if patients_id in data:
        return data[patients_id]
    raise HTTPException(status_code=404,detail='Patient not found')


#Sorting the Patients data
@app.get('/sort')
def sort_patients(sort_by: str=Query(...,description='Sort on the basis of Height, weight or bmi'),order: str=Query('asc',description='Sort in asc or desc order')):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field. Select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select from asc or desc')
    
    data=load_data()
    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    return sorted_data


#Create 
@app.post('/create')
def create_patient(patient: Patient):
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})


#Update
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')

    existing_patient_info=data[patient_id]

    #to make the patient pydantic object a dic
    #with only the updated fields not all hence unset is true
    updated_patient_info=patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_object.model_dump(exclude='id')
    
    data[patient_id]=existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient updated successfully'})

#Delete
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})