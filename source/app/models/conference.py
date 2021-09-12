from datetime import date, datetime
from typing import Optional

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin

class ConferenceBase(CoreModel):
    """All common characteristics of our conference resource"""

    title: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class ConferenceCreate(ConferenceBase):
    title: str
    description: str
    start_date: date
    end_date: date

class ConferenceUpdate(ConferenceBase):
    title: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

class ConferenceInDB(DateTimeModelMixin, IDModelMixin, ConferenceBase):
    title: str
    description: str
    start_date: date
    end_date: date

class ConferencePublic(IDModelMixin, ConferenceBase):
    pass
