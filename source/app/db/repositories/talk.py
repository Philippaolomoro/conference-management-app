from typing import List
from fastapi import HTTPException, status

from app.db.repositories.base import BaseRepository
from app.models.talk import TalkCreate, TalkUpdate, TalkInDB
from app.models.conference import ConferenceInDB

CREATE_TALK_QUERY = """
    INSERT INTO talk (title, description, duration, date_time, conference)
    VALUES (:title, :description, :duration, :date_time, :conference)
    RETURNING id, title, description, duration, date_time, conference, created_at, updated_at;
"""

LIST_ALL_TALK_FOR_A_CONFERENCE = """
    SELECT id, title, description, duration, date_time, conference, created_at, updated_at
    FROM talk
    WHERE conference = :conference;
"""

UPDATE_TALK_BY_ID_QUERY = """
    UPDATE talk
    SET title       = :title,
        description = :description,
        duration    = :duration,
        date_time   = :date_time
    WHERE id = :id AND conference = :conference
    RETURNING id, title, description, duration, date_time, conference, created_at, updated_at
"""


class TalkRepository(BaseRepository):
    async def create_talk(self, * new_talk: TalkCreate, requesting_conference: ConferenceInDB) -> TalkInDB:
        try:
            talk = await self.db.fetch_one(
                query=CREATE_TALK_QUERY, values={**new_talk.dict(), "conference":requesting_conference.id}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")

        return TalkInDB(**talk)

    async def list_all_conference_talk(self, requesting_conference: ConferenceInDB) -> List[TalkInDB]:
        talk_records = await self.db.fetch_all(
            query=LIST_ALL_TALK_FOR_A_CONFERENCE, value={"conference": requesting_conference.id}
        )

        return [TalkInDB(**l) for l in talk_records]

    async def update_talk(
        self, *, id: int, talk_update: TalkUpdate, requesting_conference: ConferenceInDB
    ) -> TalkInDB:
        talk = await self.db.get_talk_by_id(id=id, requesting_conference=requesting_conference)
        if not talk:
            return None

        talk_update_params = talk.copy(update=talk_update.dict(exclude_unset=True))

        updated_talk = await self.db.fetch_one(
            query=UPDATE_TALK_BY_ID_QUERY,
            values={
                **talk_update_params.dict(exclude={"created_at", "updated_at"}),
                "conference": requesting_conference.id
            },
        )

        return TalkInDB(**updated_talk)
