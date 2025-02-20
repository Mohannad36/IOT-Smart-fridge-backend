import redis
import sqlalchemy
import json

from workspace import getConfigAttribute

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

from sqlalchemy import func

from sqlalchemy.orm import Session

from .models import db, Users, Fridges, Sensors, Connections

sqlEngine = sqlalchemy.create_engine(getConfigAttribute("RestlessDatabaseFilePath"))
redisUrl = f"rediss://:{getConfigAttribute('RedisSecret')}@unified-amoeba-17090.upstash.io:6379"

fridgeGUID: str = getConfigAttribute("GUID")

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

    fridgeSpecificationAsJson: dict = redisConnection.get("StandardFridge").decode("utf-8")

    redisConnection.close()

    stmt = insert(Fridges).values(fridge_guid = fridgeGUID,
                                  model = fridgeSpecificationAsJson).on_conflict_do_nothing(index_elements=["fridge_guid"])
    with Session(engine) as session:
        success = True if session.execute(stmt).rowcount == 1 else False
        session.commit()
    return success

def insertSensorValue(sensorGuid: str,
                      sensorType: str,
                      sensorValue: float,
                      fridgeGuid = fridgeGUID,
                      engine = sqlEngine) -> bool:
    success: bool = False

    stmt = select(func.count()).select_from(Sensors).where(sensor_guid == sesnsorGuid)

    sensorExists: bool
    with Session(engine) as session:
        sensorExists = True if session.execute(stmt).scalar_one() > 0 else False

        if sensorExists:
            stmt = update(Sensors).where(Sensors.sensor_guid == sensorGuid).values(sensor_type = sensorType,
                                                                                   value = sensorValue)
            session.execute(stmt)
            session.commit()
        else:
            stmt = insert(Sensors).values(sensor_guid = sensorGuid,
                                          sensor_type = sensorType,
                                          value = sensorValue,
                                          fridge_guid = fridgeGuid)
            session.execute(stmt)
            session.commit()
    return success

def insertNewConnection(username,
                        fridgeGuid = fridgeGUID,
                        engine = sqlEngine) -> bool:
    success: bool = False

    with Session(engine) as session:
        result = session.scalars(select(Users).where(username == username)).first()
        if result != None:
            stmt = select(func.count()).select_from(Connections).where(Connections.user_id == result.user_id)
            userFound = True if session.execute(stmt).scalar_one() > 0 else False

            if not userFound:
                stmt = insert(Connections).values(fridge_guid = fridgeGuid,
                                                  user_id = result.user_id)
                session.execute(stmt)
                session.commit()

            stmt = update(Users).where(Users.username == username).values(active = True)
            session.execute(stmt)
            session.commit()
    return success

def deleteExistingConnection(userId,
                             engine = sqlEngine):
    success: bool = False

    with Session(engine) as session:
        stmt = delete(Connections).where(Connections.user_id == userId)
        session.execute(stmt)
        session.commit()

        stmt = update(Users).where(Users.user_id == userId).values(active = False)
        session.execute(stmt)
        session.commit()
    return success

def selectUserUsingUsername(username,
                            engine = sqlEngine):
    result: any = None
    with Session(engine) as session:
        result = session.scalars(select(Users).where(username == username)).first()
        if result != None:
            return result
    return result









