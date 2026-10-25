#this python class represents databse models/tables
from sqlalchemy import Integer,String,Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class SkillGroup(Base):
    __tablename__="skill_groups"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    floor_number=Column(Integer,nullable=False)

    trainers=relationship('Trainer',back_populates='skill_groups')
class Trainer(Base):
    __tablename__="trainers"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    designation=Column(Integer,nullable=False)
    session_fee=Column(Integer,nullable=False)
    experience_years=Column(Integer,nullable=False)
    skill_groups_id=Column(Integer, ForeignKey('skill_groups.id'),nullable=False)

    skill_group=relationship('SkillGroup',back_populates='trainers')

