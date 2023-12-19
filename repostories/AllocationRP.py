import datetime
from typing import List

from sqlalchemy import Update, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import repostories.UserRP
from BaseModels import AllocationBaseModel, Details
from database.DatabaseModels import Car, User, History
from repostories.UserRP import UserNotFoundError
from repostories.CarRP import IdentifierNotFoundError
from database.MainDB import mainEngine
from repostories.CarRP import ArgumentError
from servers.UserService import getUserById
from servers.CarService import getCarById, allocate, deAllocate
from database.DatabaseModels import Car, User


class AllocationRP:
    @staticmethod
    def validationArguments(allocationModel: AllocationBaseModel):
        pass

    @staticmethod
    def toHistoryModel(list_item):

        def item_to_base_model(item: History):
            return AllocationBaseModel(**item.__dict__)

        map_ = map(item_to_base_model, list_item)
        return list(map_)

    @staticmethod
    def addAllocation(allocationModel: AllocationBaseModel):

        """
        :raise Argument Error
        :param allocationModel:
        :return:
        """

        try:
            user_ = getUserById(allocationModel.id_user)
            car = getCarById(allocationModel.id_car)
        except (UserNotFoundError, IdentifierNotFoundError) as e:
            raise ArgumentError(e.message)
        # just check if the user exists and the car ether

        if not car.is_active_car:
            raise ArgumentError('The Car is Not Active Currently')

        if car.is_allocated_car:
            raise ArgumentError('The Car is Allocated Currently')

        if user_.is_banned:
            raise repostories.UserRP.ArgumentError('User Currently Banned')

        if not user_.is_active:
            raise repostories.UserRP.ArgumentError('User Currently Not Active')

        history = History(id_user=allocationModel.id_user, id_car=allocationModel.id_car, is_dup=allocationModel.is_dup,
                          ret_date=allocationModel.ret_date, price_=allocationModel.price_)

        with Session(mainEngine) as session:
            session.add(history)
            cause = ""
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                cause = e.detail

        if len(cause) > 0:
            raise ArgumentError(cause)
        allocate(allocationModel.id_car)

        return AllocationBaseModel(**session.query(History).all()[-1].__dict__)

    @staticmethod
    def disAllocate(id_: int):
        """
        :raise Argument Error
        :param id_:
        :return:
        """

        allocation: History = AllocationRP._getHistoryById(id_)
        allocation.is_active = False
        if allocation is None:
            raise ArgumentError(f"There Is No Allocation With id: {id_}")

        deAllocate(allocation.id_car)

        cause = ""
        with Session(mainEngine) as s:
            try:
                s.commit()
            except IntegrityError as e:
                s.rollback()
                cause = e.detail

        if len(cause):
            raise ArgumentError(cause)

        return Details(detail="Car Deallocate")

    @staticmethod
    def getAllHistory():
        history_ = None

        with Session(mainEngine) as session:
            return AllocationRP.toHistoryModel(session.query(History).order_by(desc(History.get_date)).all())

    @staticmethod
    def getHistoryOfUser(id_: int):
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.id_user == id_).order_by(desc(History.get_date)).all()
        return AllocationRP.toHistoryModel(ret)

    @staticmethod
    def getHistoryOfCar(id_: int):
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.id_car == id_).order_by(desc(History.get_date)).all()
        return AllocationRP.toHistoryModel(ret)

    @staticmethod
    def getHistory(id_user: int, id_car: int, date_: datetime.datetime):
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.id_car == id_car).filter(History.id_user == id_user).filter(
                History.get_date == date_).first()
        return AllocationBaseModel(**ret.__dict__)

    @staticmethod
    def getHistoryById(id_: int):
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.id_history == id_).first()

        if ret is None:
            raise ArgumentError(f'History With Id {id_} Not Found')
        return AllocationBaseModel(**ret.__dict__)

    @staticmethod
    def getAllActiveHistory():
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.is_active == 1).order_by(desc(History.get_date)).all()
        return AllocationRP.toHistoryModel(ret)

    @staticmethod
    def _getHistoryById(id_: int):
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.id_history == id_).first()
        if ret is None:
            raise ArgumentError(f'History With Id {id_} Not Found')

        return ret

    @staticmethod
    def disActiveHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_active: 0})
        with Session(mainEngine) as session:
            session.execute(statement)
            cause = ""
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                cause = e.detail
            if len(cause) > 0:
                raise ArgumentError(cause)

        return Details(detail='History DisActive')

    @staticmethod
    def getAllActiveHistory():
        ret = None
        with Session(mainEngine) as session:
            ret = session.query(History).filter(History.is_active == 1).order_by(desc(History.get_date)).all()

        return AllocationRP.toHistoryModel(ret)

    @staticmethod
    def reActiveHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_active: 1})
        with Session(mainEngine) as session:
            session.execute(statement)
            session.commit()
        return Details(detail="History Active")

    @staticmethod
    def addTrackToHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_dup: 1})
        with Session(mainEngine) as session:
            session.execute(statement)
            session.commit()

        return Details(detail="History Tracked")

    @staticmethod
    def removeTrack(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_dup: 0})
        with Session(mainEngine) as session:
            session.execute(statement)
            isError = False
            cause = ""
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                isError = True
                cause = e.detail

        if isError:
            raise ArgumentError(cause)

        return Details(detail="History Untracked")

    @staticmethod
    def getBlackHistory():
        with Session(mainEngine) as session:
            return AllocationRP.toHistoryModel(session.query(History).filter(History.is_active == 1).filter(
                History.ret_date < datetime.datetime.now()).all())


if __name__ == '__main__':
    print(AllocationRP.addAllocation(
        AllocationBaseModel(id_car=7, id_user=3, ret_date=datetime.datetime.now() + datetime.timedelta(days=3),
                            price_=34.32)))
    # # # AllocationRP.disAllocate(7)

    AllocationRP.addTrackToHistory(9)
    # history_ = AllocationRP.getAllHistory()
    # print(AllocationRP.getBlackHistory())

    # print(AllocationRP.getAllHistory())
    # history_new = AllocationRP.getHistory(history_[0].id_user, history_[0].id_car,
    #                                       datetime.datetime(2023, 11, 22, 19, 52, 33))
