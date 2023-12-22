import uvicorn
from fastapi import FastAPI
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

@app.get('/applicant/')
async def applicant():
    applicant = db.session.query(ModelApplicant).all()
    return applicant

@app.post('/admin/', response_model=SchemaAdmin)
async def admin_(admin_: SchemaAdmin):
    db_admin = ModelAdmin(admin_name=admin_.admin_name, teacher_id=admin_.competition_id)
    db.session.add(db_admin)
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

@app.get('/competition/')
async def competition():
    competition = db.session.query(ModelCompetition).all()
    return competition

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='local', port=8000)