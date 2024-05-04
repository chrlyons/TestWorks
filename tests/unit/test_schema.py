import pytest
from pydantic import ValidationError

from backend.schema import UserCreate, ReportCreate, Report, ReportSchema


@pytest.mark.unit
@pytest.mark.schema
class TestSchema:

    def test_user_create_valid(self):
        user = UserCreate(username="johndoe", name="John Doe")
        assert user.username == "johndoe"
        assert user.name == "John Doe"

    def test_user_create_invalid(self):
        with pytest.raises(ValidationError):
            UserCreate(username=123, name=456)

    def test_report_create_valid(self):
        report = ReportCreate(name="Weekly", data="Report Data")
        assert report.name == "Weekly"
        assert report.data == "Report Data"

    def test_report_create_invalid(self):
        with pytest.raises(ValidationError):
            ReportCreate(name="Weekly", data=None)

    def test_report_valid(self):
        report = Report(id=1, name="Monthly")
        assert report.id == 1
        assert report.name == "Monthly"

    def test_report_invalid(self):
        with pytest.raises(ValidationError):
            Report(id="one", name=123)

    def test_report_schema_valid(self):
        report = ReportSchema(id=1, name="Annual", data="Data")
        assert report.id == 1
        assert report.name == "Annual"
