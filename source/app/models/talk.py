from typing import List, Optional, Union
from datetime import time, datetime

from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from app.models.conference import ConferencePublic


class TalkBase(CoreModel):
    title: Optional[str]
    description: Optional[str]
    duration: Optional[time]
    date_time: Optional[datetime]


class TalkCreate(TalkBase):
    title: str
    description: str
    duration: time
    date_time: datetime


class TalkUpdate(TalkBase):
    title: Optional[str]
    description: Optional[str]
    duration: Optional[time]
    date_time: Optional[datetime]


class TalkInDB(IDModelMixin, DateTimeModelMixin, TalkBase):
    conference: int
    title: str
    description: str
    duration: time
    date_time: datetime


class TalkPublic(TalkInDB):
    conference: Union[int, ConferencePublic]
