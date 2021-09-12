from typing import List
from fastapi import HTTPException

from app.db.repositories.base import BaseRepository
from app.models.conference import ConferenceCreate, ConferenceUpdate, ConferenceInDB

CREATE_CONFERENCE_QUERY = """
    INSERT INTO conference (title, description, start_date, end_date)
    VALUES (:title, :description, :start_date, :end_date)
    RETURNING id, title, description, start_date, end_date;
"""

GET_CONFERENCE_BY_ID_QUERY = """
    SELECT id, title, description, start_date, end_date, created_at,updated_at
    FROM conference
    WHERE id = :id;
"""

GET_ALL_CONFERENCE_QUERY = """
    SELECT id, title, descriptiom, start_date, end_date, created_at, updated_at
    FROM conference;
"""

UPDATE_CONFERENCE_BY_ID_QUERY = """
    UPDATE conference
    SET title       = :title
        description = :description
        start_date  = :start_date
        end_date    = :end_date
    WHERE id = :id
    RETURNING id, title, description, start_date, end_date
"""

class ConferenceRepository(BaseRepository):
    """
    All database actions associated with the Conference resource
    """

    async def create_conference(self, *, new_conference: ConferenceCreate) -> ConferenceInDB:
        try:
            query_values = new_conference.dict()
            conference = await self.db.fetch_one(query=CREATE_CONFERENCE_QUERY, values=query_values)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")

        return ConferenceInDB(**conference)

    async def get_conference_by_id(self, *, id: int,) -> ConferenceInDB:
        conference = await self.db.fetch_one(
            query=GET_CONFERENCE_BY_ID_QUERY, values={"id": id})

        if not conference:
            return None

        return ConferenceInDB(**conference)

    async def get_all_conference(self) -> List[ConferenceInDB]:
        conference_records = await self.db.fetch_all(
            query=GET_ALL_CONFERENCE_QUERY,
        )

        return [ConferenceInDB(**l) for l in conference_records]

    async def update_conference(
        self, *, id: int, conference_update: ConferenceUpdate,
    ) -> ConferenceInDB:
        conference = await self.get_conference_by_id(id=id)

        if not conference:
            return None

        conference_update_params =  conference.copy(
            update=conference_update.dict(exclude_unset=True),
        )

        if conference_update_params.conference_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid conference type. Cannot be done",
            )

        try:
            updated_conference = await self.db.fetch_one(
                query=UPDATE_CONFERENCE_BY_ID_QUERY,
                values=conference_update_params.dict()
            )
            return ConferenceInDB(**updated_conference)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid update params",
            )
