import redis
import sqlalchemy
import json

from workspace import getConfigAttribute

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select

from sqlalchemy import func

from sqlalchemy.orm import Session

from .models import db, Users, Fridges

sqlEngine = sqlalchemy.create_engine(getConfigAttribute("RestlessDatabaseFilePath"))
redisUrl = f"rediss://:{getConfigAttribute('RedisSecret')}@unified-amoeba-17090.upstash.io:6379"

def checkIfUserExists(username: str, pincode: int,
                      engine = sqlEngine) -> bool:
    userFound: bool = False
    stmt = select(func.count()).select_from(Users).where(Users.username == username).where(Users.pincode == pincode)

    with Session(engine) as session:
        userFound = True if session.execute(stmt).scalar_one() > 0 else False
    return userFound


def insertNewFridgeIfNotExists(engine = sqlEngine) -> bool:
    success: bool = False
    redisConnection: redis.Redis = redis.from_url(redisUrl)

    fridgeGUID: str = getConfigAttribute("GUID")
    fridgeSpecificationAsJson: dict = redisConnection.get("StandardFridge").decode("utf-8")

    redisConnection.close()

    stmt = insert(Fridges).values(fridge_guid = fridgeGUID,
                                  model = fridgeSpecificationAsJson).on_conflict_do_nothing(index_elements=["fridge_guid"])
    with Session(engine) as session:
        success = True if session.execute(stmt).rowcount == 1 else False
        session.commit()
    return success







