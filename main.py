import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Applicant as SchemaApplicant
from schema import Admin as SchemaAdmin
from schema import Competition as SchemaCompetition

from schema import Applicant
from schema import Admin
from schema import Competition

from models import Applicant as ModelApplicant
from models import Admin as ModelAdmin
from models import Competition as ModelCompetition

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/applicant/', response_model=SchemaApplicant)
async def applicant(applicant: SchemaApplicant):
    db_applicant = ModelApplicant(applicant_name=applicant.applicant_name, admin_id=applicant.admin_id)
    db.session.add(db_applicant)
    db.session.commit()
    return db_applicant

@app.put('/applicant/{applicant_id}', response_model=SchemaApplicant)
async def update_applicant(applicant_id: int, updated_applicant: SchemaApplicant):
    db_applicant = db.session.query(ModelApplicant).filter(ModelApplicant.id == applicant_id).first()
    if db_applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    for field, value in updated_applicant.dict().items():
        setattr(db_applicant, field, value)
    db.session.commit()
    return db_applicant

@app.delete('/applicant/{applicant_id}', response_model=SchemaApplicant)
async def delete_applicant(applicant_id: int):
    db_applicant = db.session.query(ModelApplicant).filter(ModelApplicant.id == applicant_id).first()
    if db_applicant:
        db.session.delete(db_applicant)
        db.session.commit()
        return db_applicant
    raise HTTPException(status_code=404, detail="Applicant not found")

@app.get('/applicant/')
async def applicant():
    applicant = db.session.query(ModelApplicant).all()
    return applicant

@app.post('/admin/', response_model=SchemaAdmin)
async def admin_(admin_: SchemaAdmin):
    db_admin = ModelAdmin(admin_name=admin_.admin_name, competition_id=admin_.competition_id)
    db.session.add(db_admin)
    db.session.commit()
    return db_admin

@app.delete('/admin/{admin_id}', response_model=SchemaAdmin)
async def delete_admin(admin_id: int):
    db_admin = db.session.query(ModelAdmin).filter(ModelAdmin.id == admin_id).first()
    if db_admin:
        db.session.delete(db_admin)
        db.session.commit()
        return db_admin
    raise HTTPException(status_code=404, detail="Admin not found")

@app.put('/admin/{admin_id}', response_model=SchemaAdmin)
async def update_admin(admin_id: int, updated_admin: SchemaAdmin):
    db_admin = db.session.query(ModelAdmin).filter(ModelAdmin.id == admin_id).first()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    for field, value in updated_admin.dict().items():
        setattr(db_admin, field, value)
    db.session.commit()
    return db_admin

@app.get('/admin/')
async def admin_():
    admin_ = db.session.query(ModelAdmin).all()
    return admin_

@app.post('/competition/', response_model=SchemaCompetition)
async def competition(competition:SchemaCompetition):
    db_competition = ModelCompetition(competition_name=competition.competition_name)
    db.session.add(db_competition)
    db.session.commit()
    return db_competition

@app.delete('/competition/{competition_id}', response_model=SchemaCompetition)
async def delete_competition(competition_id: int):
    db_competition = db.session.query(ModelCompetition).filter(ModelCompetition.id == competition_id).first()
    if db_competition:
        db.session.delete(db_competition)
        db.session.commit()
        return db_competition
    raise HTTPException(status_code=404, detail="Competition not found")

@app.put('/competition/{competition_id}', response_model=SchemaCompetition)
async def update_competition(competition_id: int, updated_competition: SchemaCompetition):
    db_competition = db.session.query(ModelCompetition).filter(ModelCompetition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    db_competition.competition_name = updated_competition.competition_name
    db.session.commit()
    return db_competition


@app.get('/competition/')
async def competition():
    competition = db.session.query(ModelCompetition).all()
    return competition

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='local', port=8000)