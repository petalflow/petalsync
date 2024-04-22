
from api.config.dbConfig import router
from api.schemas.schemas import TagModel, TagSaveModel
from api.model.db import Tag

from typing import List


@router.post("/tags/", response_model=TagModel, tags=['Project'])
def create_tag(tag: TagSaveModel):
    new_tag = Tag(
        name=tag.name
        )
    new_tag.save()  
    return TagModel(id_tag=new_tag.id, name=new_tag.name)

@router.get("/tags/", response_model=List[TagModel], tags=['Project'])
def get_tags():
    tags = Tag.objects().all()
    all_tags = [
        TagModel(
            id_tag=tag.id_tag,
            name=tag.name
        )
        for tag in tags
    ]
    return all_tags