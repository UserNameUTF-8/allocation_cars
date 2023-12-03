from BaseModels import AllocationBaseModel, Details, AdminResponseBaseModel
from repostories.CarRP import ArgumentError
from servers.AllocationService import getHistoryOfCar, getAllHistory, getAllocationOfUser, \
    allocateCar, disActivateAllocation, getBlackHistory, addTrackerToHistory, removeTrack, getHistory, \
    getAllActiveHistory
from fastapi import APIRouter, HTTPException, status, Depends
from controllers.AdminController import getCurrentAdmin

allocationRouter = APIRouter(prefix="/allocate")


@allocationRouter.post('/')
def allocate(all_: AllocationBaseModel, currentAdmin=Depends(getCurrentAdmin)):
    if currentAdmin.authority > 1:
        raise ArgumentError('Request Not Allowed')
    try:
        allocateCar(all_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return Details(detail="Car Allocated")


@allocationRouter.put('/')
def unAllocate(id_: int, currentAdmin=Depends(getCurrentAdmin)):
    if currentAdmin.authority > 1:
        raise ArgumentError('Request Not Allowed')

    try:
        disActivateAllocation(id_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return Details(detail="Car Dis-allocated")


@allocationRouter.get('/')
def historyAll(currentAdmin=Depends(getCurrentAdmin)):
    return getAllHistory()


@allocationRouter.get('/active/all')
def allActiveHistory(currentAdmin=Depends(getCurrentAdmin)):
    return getAllActiveHistory()


@allocationRouter.get('/{id_}')
def historyById(id_: int, currentAdmin=Depends(getCurrentAdmin)):
    try:
        return getHistory(id_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@allocationRouter.get('/user/{id_user}')
def userHistory(id_user: int, currentAdmin=Depends(getCurrentAdmin)):
    return getAllocationOfUser(id_user)


@allocationRouter.get('/car/{id_car}')
def carHistory(id_car: int, currentAdmin=Depends(getCurrentAdmin)):
    return getHistoryOfCar(id_car)


@allocationRouter.get('/back/all')
def blackHistory(currentAdmin=Depends(getCurrentAdmin)):
    return getBlackHistory()


@allocationRouter.put('/track/{id_}')
def addTrackToHistory(id_: int, currentAdmin: AdminResponseBaseModel = Depends(getCurrentAdmin)):
    if currentAdmin.authority > 1:
        raise ArgumentError('Request Not Allowed')
    return addTrackerToHistory(id_)


@allocationRouter.put('/untrack/{id_}')
def addTrackToHistory(id_: int, currentAdmin=Depends(getCurrentAdmin)):
    if currentAdmin.authority > 1:
        raise ArgumentError('Request Not Allowed')
    return removeTrack(id_)
