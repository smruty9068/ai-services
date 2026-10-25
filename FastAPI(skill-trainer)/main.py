from fastapi import FastAPI,Depends,HTTPException #Depends, gets something that our function needs
from sqlalchemy.orm import Session #Session represents the type of database session to endpoint users

import models
import schemas

from database import engine,get_db#engine is connected/configured for learning.db
#get_db gives an API request, a database system

models.Base.metadata.create_all(bind=engine)#creating the registered tables in models

app=FastAPI()#start my api application

#next we will create the end points, @app.get(),@app.post(),@app.put()...

#endpoint 1-create the skill group
@app.post("/skill-groups",response_model=schemas.SkillGroupOut,status_code=201) #response model-it should follow the SkillGroupOut structure
def create_skill_group(data:schemas.SkillGroupCreate,db:Session=Depends(get_db)): #data:... is the incoming req. body, db.Session..-gives this func a database session called db
    new_group=models.SkillGroup(name=data.name,floor_number=data.floor_number)#the database objects are created
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group #FastAPI/Pydantic converts this ORM object, into SkillGroupOut.

#endpoint 2-create Trainer
@app.post("/skill-groups/{parent_id}/trainers",response_model=schemas.TrainerOut,status_code=201)
def create_trainer(parent_id:int,data:schemas.TrainerCreate,db:Session=Depends(get_db)):
    parent=(db.query(models.SkillGroup).filter(models.SkillGroup.id==parent_id).first())
    if parent is None:
        raise HTTPException(status_code=404,detail="Skill group not found")
    new_trainer=models.Trainer(name=data.name,designation=data.designation,session_fee=data.session_fee,experience_years=data.experience_years,skillgroup_id=parent_id)
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    return new_trainer

#endpoint 3-GET SKILLGROUP + TRAINER
#Get trainers,WHERE skillgroup_id = 1 AND designation = Senior
@app.get("/skill-groups/{parent_id}",response_model=schemas.SkillGroupWithTrainers)
def get_skill_group(parent_id: int,designation: str | None = None,sort: str | None = None,db: Session = Depends(get_db)):
    parent = (db.query(models.SkillGroup).filter(models.SkillGroup.id == parent_id).first()
    )
    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Skill group not found"
        )#finding the parent
    trainer_query = (
        db.query(models.Trainer)
        .filter(models.Trainer.skillgroup_id == parent_id)
    )#finding the trainers belonging to the skill group
    if designation is not None and designation.strip()!="":
        trainer_query=trainer_query.filter(models.Trainer.designation==designation)
    if sort is not None:
        if sort=='name':
            trainer_query=trainer_query.order_by(models.Trainer.name.asc())
        elif sort=='session_fee':
            trainer_query=trainer_query.order_by(models.Trainer.session_fee.asc())
        else:
            raise HTTPException(status_code=404,detail="Invalid sort field")
    trainers=trainer_query.all()#give all matching trainers
    return {'id':parent.id,'name':parent.name,'floor_number':parent.floor_number,'trainers':trainers}

#update trainer 4 who should belong to skill group 1 -> parent_id=1,child_id=4
@app.put("/skill-group/{parent_id}/trainers/{child_id}",response_model=schemas.TrainerOut,status_code=200)
def update_trainer(parent_id:int, child_id:int, data:schemas.TrainerCreate,db:Session=Depends(get_db)):
    parent=(db.query(models.SkillGroup.id==parent_id).first())
    if parent is None:
        raise HTTPException(status_code=404,detail="Skill group not found")
    trainer=(
        db.query(models.Trainer).filter(models.Trainer.id==child_id,models.Trainer.skillgroup_id==parent_id).first())
    if tariner is None:
        raise HTTPException(status_code=404,detail="Trainer not found")

    trainer.name=data.name
    trainer.designation=data.designation
    trainer.session_fee=data.session_fee
    trainer.experience_years=data.experience_years

    db.commit()
    db.refresh(trainer)
    return trainer

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080
    )