from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.login import login_router
from backend.routes.reports import report_router
from backend.routes.users import user_router

from backend.database import engine
from backend.models import Base

app = FastAPI()


origins = ["http://127.0.0.1:3000", "http://localhost:3000", "http://frontend:3000, http://0.0.0.0:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def startup_event():
    Base.metadata.create_all(bind=engine)


def shutdown_event():
    pass


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


app.include_router(login_router)
app.include_router(report_router, prefix="/api")
app.include_router(user_router, prefix="/api")
