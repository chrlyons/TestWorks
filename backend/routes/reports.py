from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import Report
from backend.database import get_db
from backend.schema import ReportCreate, ReportSchema

report_router = APIRouter(prefix="/reports")


@report_router.post("/{user_id}")
def create_report(user_id: int, report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(name=report.name, data=report.data, user_id=user_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@report_router.get("/{user_id}/{report_id}", response_model=ReportSchema)
def get_report(user_id: int, report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == user_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
