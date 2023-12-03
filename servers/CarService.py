from repostories.CarRP import CarRP, ArgumentError, IdentifierFound, IdentifierNotFoundError
from BaseModels import CarUpdateBaseModel, AddCarBaseModel, CarResponseBaseModel


# CRUD SECTION

def addCar(new_car: AddCarBaseModel):
    return CarRP.addCar(new_car)


def updateCar(model_car_to_update: CarUpdateBaseModel):
    return CarRP.updateCar(model_car_to_update)


def deleteCar(id_: int | str):
    """
    :param id_ : it could be identifier or id
    :return:
    """
    return CarRP.deleteCar(id_)


# GET SECTION

def getCarById(id_: int):
    return CarRP.getCarById(id_)


def getNumberOfCars():
    return CarRP.getNumberCars()


def getAllModels():
    return CarRP.getModelsAvailable()


def getAllCars():
    return CarRP.getAllCars()


def getActiveCars():
    return CarRP.getAllActiveCars()


def getAllAvailableCars():
    return CarRP.getAllAvailableCars()


def getAllAvailableCarsWithColor(color: str):
    return CarRP.getAvailableCarsWithColor(color)


def getAllAvailableCarsWithModel(model: str):
    return CarRP.getAvailableCarWithModel(model)


def getAllAvailableCarsWithModelWithColor(model: str, color: str):
    return CarRP.getAvailableCarWithModelWithColor(model, color)


# ACTIVATION SECTION

def activeCar(id_: int):
    return CarRP.reActive(id_)


def disActiveCar(id_: int):
    return CarRP.disActive(id_)


# ALLOCATION SECTION

def allocate(id_: int):
    return CarRP.allocate(id_)


def deAllocate(id_: int):
    return CarRP.diAllocate(id_)
