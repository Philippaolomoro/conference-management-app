from fastapi import FastAPI, HTTPException, Depends, Path

from app.models.conference import ConferenceInDB
from app.db.repositories.conference import ConferenceRepository

from app.api.dependencies.database import get_repository


async def get_conference_by_id_from_path(
    conference_id: int = Path(..., ge=1),
    conference_repo: ConferenceRepository = Depends(get_repository(ConferenceRepository)),
) -> ConferenceInDB:
    conference = await conference_repo.get_conference_by_id(id=conference_id,)

    if not conference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No conference found with that id"
        )

    return conference
