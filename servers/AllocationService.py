import datetime

from repostories.AllocationRP import AllocationRP
from repostories.CarRP import CarRP
from BaseModels import AllocationBaseModel


def allocateCar(all_: AllocationBaseModel):
    """
    :raise Argument Error
    :param all_:
    :return:
    """

    response = AllocationRP.addAllocation(all_)
    if response:
        CarRP.allocate(all_.id_car)


def getAllocationOfUser(id_user: int):
    res = AllocationRP.getHistoryOfUser(id_user)
    return res


def getAllActiveHistory():
    return AllocationRP.getAllActiveHistory()


def getAllHistory():
    return AllocationRP.getAllHistory()


def getHistoryOfCar(id_: int):
    return AllocationRP.getHistoryOfCar(id_)


def getHistory(id_: int):
    return AllocationRP.getHistoryById(id_)


def getHistoryUserCar(id_user: int, id_car: int, date: datetime.datetime):
    return AllocationRP.getHistory(id_user, id_car, date)


def disActivateAllocation(id_: int):
    """
    : raise Argument Error
    :param id_:
    :return:
    """

    return AllocationRP.disAllocate(id_)


def getBlackHistory():
    return AllocationRP.getBlackHistory()


def addTrackerToHistory(id_: int):
    """
    :raise Argument Error
    :param id_:
    :return:
    """
    return AllocationRP.addTrackToHistory(id_)


def removeTrack(id_):
    """
    :raise Argument Error
    :param id_:
    :return:
    """

    return AllocationRP.removeTrack(id_)


if __name__ == '__main__':
    # allocateCar(AllocationBaseModel(id_car=1, id_user=3, ret_date=datetime.datetime.now() + datetime.timedelta(
    #     days=10), price_=3421.34))
    # disActivateAllocation(9)
    pass
