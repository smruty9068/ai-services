#here we have pydantics:
#--create-what user sends
#--out-what API sends back
from pydantic import BaseModel,ConfigDict,Field

class TrainerCreate(BaseModel):
    name:str=Field(min_length=1)
    designation:str=Field(min_length=1)
    session_fee:int=Field(ge=301) #gt=300
    experience_years:int=Field(ge=1) #gt=0
class TrainerOut(BaseModel):
    id:int
    name:str
    designation:str
    session_fee:int
    experience_years:int

    model_config=ConfigDict(from_attributes=True)

class SkillGroupCreate(BaseModel):
    name:str=Field(min_length=1)
    floor_number:int=Field(min_length=1)
class SkillGroupOut(BaseModel):
    id:int
    name:str
    floor_number:int
    
    model_config=ConfigDict(from_attributes=True)

class SkillGroupWithTrainers(BaseModel):
    id:int
    name:str
    floor_number:int
    trainer:list[TrainerOut]

    model_config=ConfigDict(from_attributes=True)