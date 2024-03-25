from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
import os

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class Student_Grade(BaseModel):
    
    grade_month_1: int
    grade_month_2: int
    grade_month_3: int
    
# loading the saved model
#RFR_Model = pickle.load(open('gbR94.sav' ,'rb'))

working_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(working_dir ,'gbR82.sav')

with open(model_path, 'rb')as f:
  Model = pickle.load(f)
 
@app.post('/grades_students')
def degree_pred(input_parameters : Student_Grade ):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    dgr_mo_1 = input_dictionary['grade_month_1']
    dgr_mo_2 = input_dictionary['grade_month_2']
    dgr_mo_3 = input_dictionary['grade_month_3']
    
    input_list = [dgr_mo_1 , dgr_mo_2 , dgr_mo_3] 
    
    prediction = Model.predict([input_list])
   
    predicted_grade = {"student_grade": round(prediction[0], 1)}  
    max_grade=100
    predicted_percentage = round((predicted_grade["student_grade"] / max_grade) * 100, 1)
    formatted_result = "Student_grade: {:.1f}%".format(predicted_percentage)
    return formatted_result
    
 
    
    
    
    
    
