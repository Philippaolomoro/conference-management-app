from typing import List

from fastapi import FastAPI, APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED

from app.models.conference import ConferenceCreate, ConferencePublic, ConferenceUpdate
from app.db.repositories.conference import ConferenceRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.post("/", response_model=ConferencePublic, name="conference:create-conference", status_code=HTTP_201_CREATED)
async def create_new_conference(
    new_conference: ConferenceCreate = Body(..., embed=True),
    conference_repo: ConferenceRepository = Depends(get_repository(ConferenceRepository)),
) -> ConferencePublic:
    created_conference = await conference_repo.create_conference(new_conference=new_conference)

    return created_conference

@router.get("/", response_model=List[ConferencePublic], name="conference:get-all-conference")
async def get_all_conference(
    conference_repo: ConferenceRepository = Depends(get_repository(ConferenceRepository))
) -> List[ConferencePublic]:
    return await conference_repo.get_all_conference()

router.put(
    "/{id}/",
    response_model=ConferencePublic,
    name="conference:update-conference-by-id"
)
async def update_conference_by_id(
    id: int = Path(..., ge=1, title="The ID of the conference to update."),
    conference_update: ConferenceUpdate = Body(..., embed=True),
    conference_repo: ConferenceRepository = Depends(get_repository(ConferenceRepository)),
) -> ConferencePublic:
    updated_conference = await conference_repo.update_conference(
        id=id, conference_update=conference_update,
    )

    if not updated_conference:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No conference found with that id",
        )
    return updated_conference
