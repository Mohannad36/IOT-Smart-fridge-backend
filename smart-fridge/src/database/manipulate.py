import redis
import sqlalchemy

import workspace as workspace

from sqlalchemy import insert
from sqlalchemy import select

from sqlalchemy import func

from sqlalchemy.orm import Session

from .models import db, Users

redisConnection: redis.Redis = redis.Redis(host = "unified-amoeba-17090.upstash.io",
                                           port = 6379,
                                           password = workspace.getConfigAttribute("RedisSecret"),
                                           ssl = True)

def checkIfUserExists(engine, 
                      username: str, pincode: int) -> bool:
    userFound: bool = False
    stmt = select(func.count()).select_from(Users).where(Users.username == username).where(Users.pincode == pincode)

    with Session(engine) as session:
        userFound = True if session.execute(stmt).scalar_one() > 0 else False
    return userFound


def insertNewFridgeIfNotExists() -> bool:
    fridgeGUID: str = workspace.getConfigAttribute("GUID")

