from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from core.database import Base

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # create
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        data = obj_in.dict(exclude_unset=True)

        # Replace missing fields with blank string
        for field in self.model.__table__.columns:
            if field.name not in data and field.type.python_type == str:
                data[field.name] = " "

        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # get by ID

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    # update

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)

        # for field in self.model.__table__.columns:
        #     if field.name not in update_data and field.type.python_type == str:
        #         update_data[field.name] = getattr(db_obj, field.name) or " "

        # for k, v in update_data.items():
        #     setattr(db_obj, k, v if v is not None else " ")
        for key, value in update_data.items():
            if value is None:
                continue
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

 
    # delete

    def remove(self, db: Session, id: UUID) -> Optional[ModelType]:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
