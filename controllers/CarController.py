from fastapi import APIRouter, HTTPException, status
from BaseModels import CarUpdateBaseModel, CarResponseBaseModel, AddCarBaseModel
from repostories.CarRP import ArgumentError, IdentifierNotFoundError, IdentifierFound
from servers.CarService import (addCar, updateCar, deleteCar, getAllCars, getCarById, getActiveCars,
                                getAllAvailableCars, getAllAvailableCarsWithColor, getAllAvailableCarsWithModel,
                                getAllAvailableCarsWithModelWithColor, activeCar, allocate, deAllocate, disActiveCar)

carRoute = APIRouter(prefix="/cars")


@carRoute.post('/')
def addCarC(car: AddCarBaseModel):
    try:
        return addCar(car)
    except (IdentifierFound, ArgumentError,) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@carRoute.put('/')
def updateCarC(carModelToUpdate: CarUpdateBaseModel):
    try:
        return updateCar(carModelToUpdate)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@carRoute.delete('/')
def deleteCarC(id_: int):
    try:
        return deleteCar(id_)
    except IdentifierNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@carRoute.get('/')
def getAllCarsC(id_: int | None = None):
    if id_:
        try:
            return getCarById(id_)
        except IdentifierNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return getAllCars()


@carRoute.get('/active')
def getActiveCarsC():
    return getActiveCars()


@carRoute.get('/available')
def getAvailableCars(model: str = None, color: str | None = None):
    if model and color:
        return getAllAvailableCarsWithModelWithColor(model, color)
    elif model:
        return getAllAvailableCarsWithModel(model)
    elif color:
        return getAllAvailableCarsWithColor(color)
    else:
        return getAllAvailableCars()


# ACTIVE ACTIONS

@carRoute.post("/active_/{id_}")
def activeCarC(id_: int):
    return activeCar(id_)


@carRoute.post("/dis-active/{id_}")
def disActiveCarC(id_: int):
    return disActiveCar(id_)


# ALLOCATE CAR

@carRoute.post('/allocate/{id_}')
def allocateC(id_: int):
    return allocate(id_)


@carRoute.post('/de-allocated')
def deAllocatedCarC(id_: int):
    return disActiveCar(id_)
