import MySQLdb

from database.MainDB import session
from sqlalchemy import Update, Delete
from Utils import sha256
from database.DatabaseModels import Admin
from BaseModels import SignUpBaseModel, AdminUpdateBaseModel, AdminResponseBaseModel, AdminUpdatePasswordBaseModel
from sqlalchemy.exc import IntegrityError


class ArgumentError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AdminNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class MailExistsError(RuntimeError):
    def __init__(self, message='Mail Exists Error'):
        self.message = message
        super().__init__(message)


def dataValidation(adminInfo: SignUpBaseModel):
    if len(adminInfo.email_admin) < 4 or not adminInfo.email_admin.__contains__('@'):
        raise ArgumentError('Invalid Email')

    if len(adminInfo.name_admin) < 4 or len(adminInfo.name_admin) > 100:
        raise ArgumentError('Invalid Name')

    if len(adminInfo.password_admin) < 8:
        raise ArgumentError('Password Too Short')

    if adminInfo.ip_admin is not None:
        if len(adminInfo.ip_admin) > 32:
            raise ArgumentError('Invalid IP Address')


class AdminRP:
    @staticmethod
    def addAdmin(adminInfo: SignUpBaseModel):
        dataValidation(adminInfo)
        adminInfo.password_admin = sha256(adminInfo.password_admin)

        new__admin = Admin(**adminInfo.__dict__)
        session.add(new__admin)
        try:
            session.commit()
        except IntegrityError:
            raise MailExistsError

        admin__ = AdminRP.getAdminByEmail(adminInfo.email_admin)

        return AdminResponseBaseModel(**admin__.__dict__)

    @staticmethod
    def getAdminById(id_: int):
        admin__ = session.query(Admin).filter(Admin.id_admin == id_).first()
        if admin__ is None:
            raise AdminNotFoundError(f'There is No Admin With Id {id_}')
        return AdminResponseBaseModel(**admin__.__dict__)

    @staticmethod
    def getAdminByEmail(email: str):
        admin__ = session.query(Admin).filter(Admin.email_admin == email).first()
        if admin__ is None:
            raise AdminNotFoundError(f'Admin With This Mail Not Exists')

        return admin__

    @staticmethod
    def updateAdmin(updateModel: AdminUpdateBaseModel):
        query_to_update = Update(Admin).where(Admin.id_admin == updateModel.id_admin)
        is_update_same_thing = False
        if updateModel.name_admin is not None:
            if len(updateModel.name_admin) > 100 or len(updateModel.name_admin) < 4:
                raise ArgumentError('Name Invalid')
            query_to_update = query_to_update.values({Admin.name_admin: updateModel.name_admin})
        is_update_same_thing = True

        if updateModel.ip_admin is not None:
            if len(updateModel.ip_admin) > 32 or len(updateModel.ip_admin) < 8:
                raise ArgumentError('Invalid IP Address')
            query_to_update = query_to_update.values({Admin.ip_admin: updateModel.ip_admin})
            is_update_same_thing = True

        if not is_update_same_thing:
            raise ArgumentError('No Argument Specified')

        session.execute(query_to_update)
        session.commit()

        admin__ = AdminRP.getAdminById(updateModel.id_admin)
        return AdminResponseBaseModel(**admin__.__dict__)

    @staticmethod
    def updatePassword(updatePassModel: AdminUpdatePasswordBaseModel):
        if len(updatePassModel.password_admin) < 8:
            raise ArgumentError('Invalid Password')

        new_password = sha256(updatePassModel.password_admin)

        query = Update(Admin).where(Admin.id_admin == updatePassModel.id_admin).values(
            {Admin.password_admin: new_password})
        session.execute(query)
        session.commit()
        return AdminRP.getAdminById(updatePassModel.id_admin)

    @staticmethod
    def deleteAdmin(id_: int | str):
        statement = Delete(Admin)
        if type(id_) is int:
            statement = statement.where(Admin.id_admin == id_)
        else:
            statement = statement.where(Admin.email_admin == id_)

        session.execute(statement)
        session.commit()
        return {"details": f"Admin With {id_} Deleted"}


if __name__ == '__main__':
    # new_admin = SignUpBaseModel(email_admin='essid01@go.com', password_admin='HelloWorld', name_admin='Amine Essid')
    # try:
    #     AdminRP.addAdmin(new_admin)
    # except MailExistsError:
    #     raise MailExistsError
    # admin_ = AdminRP.getAdminByEmail('essid01@go.com')
    # print(admin_)
    # admin_ = AdminRP.getAdminById(1)
    # print(f'this is the admin {admin_}')
    # print(AdminRP.updatePassword(AdminUpdatePasswordBaseModel(id_admin=1, password_admin="HelloMan")))
    # pass
    # print(AdminRP.updateAdmin(AdminUpdateBaseModel(id_admin=1, ip_admin='localhost')))
    pass
