import datetime
from sqlalchemy import Update
import repostories.UserRP
from BaseModels import AllocationBaseModel
from database.DatabaseModels import Car, User, History
from database.MainDB import session
from repostories.CarRP import ArgumentError
from servers.UserService import getUserById
from servers.CarService import getCarById
from database.DatabaseModels import Car, User


class AllocationRP:

    @staticmethod
    def validationArguments(allocationModel: AllocationBaseModel):
        pass

    @staticmethod
    def addAllocation(allocationModel: AllocationBaseModel):
        user_ = getUserById(allocationModel.id_user)
        car = getCarById(allocationModel.id_car)
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
        session.add(history)
        session.commit()

        return session.query(History).all()[-1]

    @staticmethod
    def getAllHistory():
        return session.query(History).all()

    @staticmethod
    def getHistoryOfUser(id_: int):
        return session.query(History).filter(History.id_user == id_).all()

    @staticmethod
    def getHistoryOfCar(id_: int):
        return session.query(History).filter(History.id_car == id_).all()

    @staticmethod
    def getHistory(id_user: int, id_car: int, date_: datetime.datetime):

        return session.query(History).filter(History.id_car == id_car).filter(History.id_user == id_user).filter(
            History.get_date == date_).first()

    @staticmethod
    def getHistoryById(id_: int):
        return session.query(History).filter(History.id_history == id_).first()

    @staticmethod
    def disActiveHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_active: 0})
        session.execute(statement)
        session.commit()

    @staticmethod
    def getAllActiveHistory():
        return session.query(History).filter(History.is_active == 1).all()

    @staticmethod
    def reActiveHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_active: 1})
        session.execute(statement)
        session.commit()

    @staticmethod
    def addTrackToHistory(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_dup: 1})
        session.execute(statement)
        session.commit()

    @staticmethod
    def removeTrack(id_: int):
        statement = Update(History).filter(History.id_history == id_).values({History.is_dup: 0})
        session.execute(statement)
        session.commit()


if __name__ == '__main__':
    # AllocationRP.addAllocation(
    #     AllocationBaseModel(id_car=4, id_user=3, ret_date=datetime.datetime.now() + datetime.timedelta(days=2),
    #                         price_=34.32))

    history_ = AllocationRP.getAllHistory()
    print(history_)
    # history_new = AllocationRP.getHistory(history_[0].id_user, history_[0].id_car,
    #                                       datetime.datetime(2023, 11, 22, 19, 52, 33))
