from BaseModels import AddUserBaseModel, UserUpdateBaseModel, UserPasswordModel, UserResponseBaseModel, Details
from repostories.UserRP import UserRP


# crud section

def createUser(new_user: AddUserBaseModel) -> UserResponseBaseModel:
    """
    :raise MailExistsError
    :param new_user:
    :return:
    """
    return UserRP.addUser(new_user)  # may Generate Error -> MailExistsError


def updateUser(user_update_model: UserUpdateBaseModel) -> UserResponseBaseModel:
    """
    :raise ArgumentError
    :param user_update_model:
    :return:
    """
    return UserRP.updatedUser(user_update_model)  # may Generate Error -> ArgumentError


def updatePasswordUser(user_update_password_model: UserPasswordModel) -> UserResponseBaseModel:
    """

    :param user_update_password_model:
    :return:
    """
    return UserRP.updatePassword(user_update_password_model)


def deleteUser(id_user_to_remove: int) -> Details:
    return UserRP.deleteUser(id_user_to_remove)  # generate Error Probably -> UserNotFoundError


def getUser(indicator: int | str) -> UserResponseBaseModel:
    if type(indicator) is int:
        return UserRP.getUserById(indicator)  # may generate Error -> UserNotFoundError
    else:
        return UserRP.getUserByEmail(indicator)  # may generate Error -> UserNotFoundError


# section get

def getUserById(id_: int) -> UserResponseBaseModel:
    return UserRP.getUserById(id_)


def getAllUsers() -> list[UserResponseBaseModel]:
    return UserRP.getAllUsers()


def getAllActiveUsers() -> list[UserResponseBaseModel]:
    return UserRP.getAllActiveUsers()


def getAllBannedUsers() -> list[UserResponseBaseModel]:
    return UserRP.getAllBannedUsers()


def getAllUsersByName(name: str) -> list[UserResponseBaseModel]:
    return UserRP.getUsersByName(name)


def searchUsers(keyword: str) -> list[UserResponseBaseModel]:
    return UserRP.searchUsersByName(keyword)


# section banne

def banneUser(id_: int) -> UserResponseBaseModel:
    return UserRP.banneUser(id_)


def deBanneUser(id_: int) -> UserResponseBaseModel:
    return UserRP.unBanneUser(id_)


# section active

def disActiveUser(id_: int) -> UserResponseBaseModel:
    return UserRP.disActiveUser(id_)


def reActiveUser(id_: int) -> UserResponseBaseModel:
    return UserRP.active(id_)
