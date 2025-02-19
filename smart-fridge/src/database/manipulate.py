import valkey
import sqlalchemy

import workspace as workspace

from sqlalchemy import insert
from sqlalchemy import select

from sqlalchemy import func

from sqlalchemy.orm import Session

from .models import db, Users

valkeyUri: str = f"valkeys://default:{workspace.getConfigAttribute('VALKEYSSECRET')}@valkey-23c3b453-smart-fridge.b.aivencloud.com:12263"
valkeyClient = valkey.from_url(valkeyUri) 

def checkIfUserExists(engine, 
                      username: str, pincode: int) -> bool:
    userFound: bool = False
    stmt = select(func.count()).select_from(Users).where(Users.username == username).where(Users.pincode == pincode)

    with Session(engine) as session:
        userFound = True if session.execute(stmt).scalar_one() > 0 else False
    return userFound


def insertNewFridgeIfNotExists() -> bool:
    fridgeGUID: str = workspace.getConfigAttribute("GUID")

