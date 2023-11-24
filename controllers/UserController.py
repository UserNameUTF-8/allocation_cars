from fastapi import APIRouter, HTTPException, status
from BaseModels import AddUserBaseModel, UserResponseBaseModel, UserUpdateBaseModel, UserPasswordModel
from servers.UserService import (createUser, updateUser, getUser, getAllUsers, getAllActiveUsers, getAllBannedUsers,
                                 updatePasswordUser,
                                 getAllUsersByName, searchUsers, deleteUser, deBanneUser, banneUser, disActiveUser,
                                 reActiveUser)

from repostories.UserRP import ArgumentError, MailExistsError, UserNotFoundError

userRouter = APIRouter(prefix='/users')


# CRUD APP

@userRouter.post('/')
def addUserC(new_user: AddUserBaseModel) -> UserResponseBaseModel:
    try:
        return createUser(new_user)  # may generate Error MailExists
    except MailExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@userRouter.put('/')
def updateUserC(model_to_updated: UserUpdateBaseModel) -> UserResponseBaseModel:
    try:
        return updateUser(model_to_updated)
    except (ArgumentError, UserNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@userRouter.delete('/')
def deleteUserByIdC(id_: int):
    try:
        return deleteUser(id_)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@userRouter.patch('/password')
def updatePasswordC(model_password_to_update: UserPasswordModel):
    return updatePasswordUser(model_password_to_update)


@userRouter.get('/{id_}')
def getUserByIdC(id_: int):
    try:
        return getUser(id_)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@userRouter.get('/mail/{mail}')
def getUserByMailC(mail: str):
    try:
        return getUser(mail)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


# GET APP

@userRouter.get('/get/all')
def getAllUsersC():
    return getAllUsers()


@userRouter.get('/all/banned')
def getAllUsersBannedC():
    return getAllBannedUsers()


@userRouter.get('/all/active')
def getAllUsersActiveC():
    return getAllActiveUsers()


@userRouter.get('/all/name/{name}')
def getAllUsersByNameC(name: str):
    return getAllUsersByName(name)


@userRouter.get('/all/search/{name}')
def searchByNameC(name: str):
    return searchUsers(name)


# ACTIVE SECTION

@userRouter.post('/user/{id_}')
def diActiveUserC(id_):
    return disActiveUser(id_)


@userRouter.post('/re-user/{id_}')
def activeUserC(id_: int):
    return reActiveUser(id_)


# BANNE SECTION

@userRouter.post('/banne/{id_}')
def banneUserC(id_: int):
    return banneUser(id_)


@userRouter.post('/de-banne/{id_}')
def deBanneUserC(id_: int):
    return deBanneUser(id_)
