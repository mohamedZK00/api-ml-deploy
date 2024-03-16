from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import pickle
import json
import numpy as np
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import uvicorn


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
RFR_Model = pickle.load(open('GBRmodel87%.PLK' ,'rb'))
 
@app.post('/grades_students')
def degree_pred(input_parameters : Student_Grade ):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    dgr_mo_1 = input_dictionary['grade_month_1']
    dgr_mo_2 = input_dictionary['grade_month_2']
    dgr_mo_3 = input_dictionary['grade_month_3']
    
    input_list = [dgr_mo_1 , dgr_mo_2 , dgr_mo_3] 
    
    prediction = RFR_Model.predict([input_list])
   
    predicted_grade = {"student_grade": round(prediction[0], 1)}  # تخمين قيمة الدرجة المتوقعة من القائمة وتقريبها لعددين عشريين
    return predicted_grade
    
 

#مشكلة في التثبيت في ال command promt
ngrok_tunnel= ngrok.connect(8000)
print("Public URL :" ,ngrok_tunnel.public_url )
nest_asyncio.apply()
uvicorn.run(app, port=8000)
    
    
    
    
    