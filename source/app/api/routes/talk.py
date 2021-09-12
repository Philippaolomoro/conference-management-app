from typing import List

from fastapi import FastAPI, APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED

from app.models.talk import TalkCreate, TalkPublic, TalkUpdate
from app.models.conference import ConferenceInDB

from app.db.repositories.talk import TalkRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.conference import get_conference_by_id_from_path


router = APIRouter()

@router.post("/", response_model=TalkPublic, name="talk:create-talk", status_code=HTTP_201_CREATED)
async def create_new_talk(
    new_talk: TalkCreate = Body(..., embed=True),
    talk_repo: TalkRepository = Depends(get_repository(TalkRepository)),
) -> TalkPublic:
    created_talk = await talk_repo.create_talk(new_talk=new_talk)

    return created_talk

@router.get("/", response_model=List[TalkPublic], name="talk:get-all-talk")
async def get_all_talk(
    talk_repo: TalkRepository = Depends(get_repository(TalkRepository))
) -> List[TalkPublic]:
    return await talk_repo.get_all_talk()

@router.get("/", response_model=List[TalkPublic], name="talk:list-all-conference-talk")
async def list_all_conference_talk(
    current_conference: ConferenceInDB = Depends(get_conference_by_id_from_path),
    talk_repo: TalkRepository = Depends(get_repository(TalkRepository)),
) -> List[TalkPublic]:
    return await talk_repo.list_all_conference_talk(requesting_conference=current_conference.id)

@router.put(
    "/{talk_id}/",
    response_model=TalkPublic,
    name="talk:update-talk-by-id"
)
async def update_talk_by_id(
    talk_id: int = Path(..., ge=1),
    current_conference: ConferenceInDB = Depends(get_conference_by_id_from_path), #TODO fill this up
    talk_update: TalkUpdate = Body(..., embed=True),
    talk_repo: TalkRepository = Depends(get_repository(TalkRepository)),
) -> TalkPublic:
    updated_talk = await talk_repo.update_talk(
        id=talk_id, talk_update=talk_update, requesting_conference=current_conference.id
    )

    if not updated_talk:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No talk found with that id",
        )
    return updated_talk
