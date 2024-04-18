from fastapi import Depends, Header, HTTPException
from typing import List
from datetime import datetime
from api.config.dbConfig import router
from api.config.dbConfig import db  # Importe a instância db do dbConfig
from api.model.db import User
from api.schemas.schemas import UserResponseModel, UserModel
import bcrypt


@router.get("/GetAllUsers", response_model=List[UserResponseModel], tags=['User'])
def get_all_users():
    Lisuser = User.objects().all()
    user_data = [
        {
            "ds_first_name": user.ds_first_name,
            "ds_last_name": user.ds_last_name,
            "ds_email": user.ds_email,
            "ds_password": user.ds_password,
            "roles": user.roles
        }
        for user in Lisuser
    ]
    return user_data



@router.post("/CreateUser", response_model=UserResponseModel, tags=['User'])   
def create_user(new_user: UserModel):
    hashed_password = bcrypt.hashpw(new_user.ds_password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        ds_first_name=new_user.ds_first_name,
        ds_last_name=new_user.ds_last_name,
        ds_email=new_user.ds_email,
        ds_password=hashed_password,  
        roles=new_user.roles
    )
    user.save()
