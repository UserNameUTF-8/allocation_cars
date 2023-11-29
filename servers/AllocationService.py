import datetime

from repostories.AllocationRP import AllocationRP
from repostories.CarRP import CarRP
from BaseModels import AllocationBaseModel


def AllocateCar(all_: AllocationBaseModel):
    response = AllocationRP.addAllocation(all_)
    if response:
        CarRP.allocate(all_.id_car)


def getAllocationOfUser(id_user: int):
    res = AllocationRP.getHistoryOfUser(id_user)
    return res


if __name__ == '__main__':
    AllocateCar(AllocationBaseModel(id_car=4, id_user=5, ret_date=datetime.datetime.now() + datetime.timedelta(days=10),
                                    price_=3421.34))
