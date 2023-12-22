# build a schema using pydantic
from pydantic import BaseModel

class Applicant(BaseModel):
    applicant_name:str
    admin_id:int

    class Config:
        from_attributes = True

class Admin(BaseModel):
    admin_name:str
    competition_id:int

    class Config:
        from_attributes = True

class Competition(BaseModel):
    competition_name:str

    class Config:
        from_attributes = True