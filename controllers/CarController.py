from fastapi import APIRouter, HTTPException, status, Depends
from BaseModels import CarUpdateBaseModel, CarResponseBaseModel, AddCarBaseModel
from repostories.CarRP import ArgumentError, IdentifierNotFoundError, IdentifierFound
from servers.CarService import (addCar, updateCar, deleteCar, getAllCars, getCarById, getActiveCars,
                                getAllAvailableCars, getAllAvailableCarsWithColor, getAllAvailableCarsWithModel,
                                getAllAvailableCarsWithModelWithColor, activeCar, allocate, deAllocate, disActiveCar,
                                getNumberOfCars, getAllModels)

from controllers.AdminController import getCurrentAdmin

carRoute = APIRouter(prefix="/cars")


@carRoute.post('/')
def addCarC(car: AddCarBaseModel, admin=Depends(getCurrentAdmin)):
    if admin.authority != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")

    try:
        return addCar(car)
    except (IdentifierFound, ArgumentError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@carRoute.put('/')
def updateCarC(carModelToUpdate: CarUpdateBaseModel, admin=Depends(getCurrentAdmin)):
    if admin.authority != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")

    try:
        return updateCar(carModelToUpdate)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@carRoute.delete('/')
def deleteCarC(id_: int, admin=Depends(getCurrentAdmin)):
    if admin.authority != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")

    try:
        return deleteCar(id_)
    except IdentifierNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@carRoute.get('/')
def getAllCarsC(id_: int | None = None, admin=Depends(getCurrentAdmin)):
    if id_:
        try:
            return getCarById(id_)
        except IdentifierNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return getAllCars()


@carRoute.get('/active')
def getActiveCarsC(admin=Depends(getCurrentAdmin)):
    return getActiveCars()


@carRoute.get('/available')
def getAvailableCars(model: str = None, color: str | None = None, admin=Depends(getCurrentAdmin)):
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
def activeCarC(id_: int, admin=Depends(getCurrentAdmin)):
    if admin.authority > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")
    return activeCar(id_)


@carRoute.post("/dis-active/{id_}")
def disActiveCarC(id_: int, admin=Depends(getCurrentAdmin)):
    if admin.authority > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")
    return disActiveCar(id_)


# ALLOCATE CAR

@carRoute.post('/allocate/{id_}')
def allocateC(id_: int, admin=Depends(getCurrentAdmin)):
    if admin.authority > 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")
    return allocate(id_)


@carRoute.post('/de-allocated')
def deAllocatedCarC(id_: int, admin=Depends(getCurrentAdmin)):
    if admin.authority > 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Request Not Allowed")

    return deAllocate(id_)


@carRoute.get('/count/all')
def getNumberOfCarsC(admin=Depends(getCurrentAdmin)):
    return getNumberOfCars()


@carRoute.get('/models')
def getAllModelsC(admin=Depends(getCurrentAdmin)):
    return getAllModels()
