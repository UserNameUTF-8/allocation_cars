from repostories import AdminRP
from BaseModels import SignUpBaseModel, AdminUpdateBaseModel, AdminUpdatePasswordBaseModel


def addAdminService(new_admin: SignUpBaseModel):
    return AdminRP.AdminRP.addAdmin(new_admin)


def getAdminById(id_: int):
    return AdminRP.AdminRP.getAdminById(id_)


def getNumberOfAdmins():
    return AdminRP.AdminRP.getAdminNumber()


def getAdminByEmail(email: str):
    return AdminRP.AdminRP.getAdminByEmail(email)


def updateAdmin(modelUpdate: AdminUpdateBaseModel):
    return AdminRP.AdminRP.updateAdmin(modelUpdate)


def updatePassword(modelPass: AdminUpdatePasswordBaseModel):
    return AdminRP.AdminRP.updatePassword(modelPass)


def deleteAdminByEmailOrId(id_: int | str):
    return AdminRP.AdminRP.deleteAdmin(id_)


def getNumberRes():
    return AdminRP.AdminRP.getNumberOfRes()
