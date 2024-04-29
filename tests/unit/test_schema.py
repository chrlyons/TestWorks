import pytest
from pydantic import ValidationError

from app.schema import UserCreate, ReportCreate, Report, ReportSchema


@pytest.mark.unit
@pytest.mark.schema
def test_user_create_valid():
    user = UserCreate(username="johndoe", name="John Doe")
    assert user.username == "johndoe"
    assert user.name == "John Doe"


@pytest.mark.unit
@pytest.mark.schema
def test_user_create_invalid():
    with pytest.raises(ValidationError):
        UserCreate(username=123, name=456)


@pytest.mark.unit
@pytest.mark.schema
def test_report_create_valid():
    report = ReportCreate(name="Weekly", data="Report Data")
    assert report.name == "Weekly"
    assert report.data == "Report Data"


@pytest.mark.unit
@pytest.mark.schema
def test_report_create_invalid():
    with pytest.raises(ValidationError):
        ReportCreate(name="Weekly", data=None)


@pytest.mark.unit
@pytest.mark.schema
def test_report_valid():
    report = Report(id=1, name="Monthly")
    assert report.id == 1
    assert report.name == "Monthly"


@pytest.mark.unit
@pytest.mark.schema
def test_report_invalid():
    with pytest.raises(ValidationError):
        Report(id="one", name=123)


@pytest.mark.unit
@pytest.mark.schema
def test_report_schema_valid():
    report = ReportSchema(id=1, name="Annual", data="Data")
    assert report.id == 1
    assert report.name == "Annual"
