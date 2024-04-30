from fastapi import FastAPI
from app.routes.users import user_router
from app.routes.reports import report_router

from app.database import engine
from app.models import Base

app = FastAPI()


def startup_event():
    Base.metadata.create_all(bind=engine)


def shutdown_event():
    pass


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


app.include_router(user_router, prefix="/api")
app.include_router(report_router, prefix="/api")
