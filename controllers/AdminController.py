import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Form

from repostories.AdminRP import AdminNotFoundError, ArgumentError
from servers import AdminService
from servers import JWTService
from Utils import sha256
from BaseModels import AdminResponseBaseModel, SignUpBaseModel, LoginBaseModel, AdminUpdatePasswordBaseModel, Details, \
    AdminUpdateBaseModel, NumbersResBaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

adminRouter = APIRouter(prefix="/admins")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")


@adminRouter.get('/res/count-res', response_model=NumbersResBaseModel)
async def getNumberRes(auth=Depends(oauth2_scheme)):
    return AdminService.getNumberRes()


@adminRouter.get('/{id_}', response_model=AdminResponseBaseModel)
async def getAdminById(id_: int, admin=Depends(oauth2_scheme)):
    try:
        return AdminService.getAdminById(id_)
    except AdminNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@adminRouter.post('/')
async def signUp(modelAdmin: SignUpBaseModel):
    try:
        return AdminService.addAdminService(modelAdmin)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


"""
    LOGIN SERVICE
"""


@adminRouter.post('/login')
async def getToken(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username Or Password Incorrect")
    admin_: AdminResponseBaseModel

    try:
        admin_ = AdminService.getAdminByEmail(credentials.username)
    except AdminNotFoundError as e:
        raise exception

    if admin_.password_admin != sha256(credentials.password):
        raise exception
    if not admin_.is_active:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Your Are Currently Not Active")

    data = {'sub': admin_.email_admin}
    data_exp = datetime.datetime.now() + datetime.timedelta(days=5)
    encoded_data = JWTService.createAccessToken(data, data_exp)
    return {"access_token": encoded_data, "token_type": "bearer", "exp_time": data_exp}


@adminRouter.get('/get/current', response_model=AdminResponseBaseModel)
async def getCurrentAdmin(adminToken=Depends(oauth2_scheme)):
    adminToken: dict = JWTService.decodeAccessToken(adminToken)
    email = adminToken.get("sub")
    admin = AdminService.getAdminByEmail(email)
    return admin


@adminRouter.get('/count/all')
async def numberOfAdmins(auth=Depends(getCurrentAdmin)):
    return AdminService.getNumberOfAdmins()


@adminRouter.patch('/')
async def update(adminNewInfo: AdminUpdateBaseModel, current_admin=Depends(getCurrentAdmin)):
    adminNewInfo.id_admin = current_admin.id_admin
    admin: AdminResponseBaseModel | None = None
    try:
        admin = AdminService.updateAdmin(adminNewInfo)
    except ArgumentError:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is No Fields To Update")

    except AdminNotFoundError:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin Not Found")

    return admin


@adminRouter.put('/password')
async def updatePassword(new_password=Form(), old_password=Form(),
                         current_admin: AdminResponseBaseModel = Depends(getCurrentAdmin)):
    if sha256(old_password) != current_admin.password_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="incorrect old password")

    new_pass = sha256(new_password)

    AdminService.updatePassword(AdminUpdatePasswordBaseModel(id_admin=current_admin.id_admin, password_admin=new_pass))

    return AdminService.getAdminById(current_admin.id_admin)


@adminRouter.delete('/', response_model=Details)
async def deleteAdmin(password_: str = Form(),
                      current_admin: AdminResponseBaseModel = Depends(getCurrentAdmin)) -> Details:
    if sha256(password_) == current_admin.password_admin:
        AdminService.deleteAdminByEmailOrId(current_admin.id_admin)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forget Password")

    return Details(detail="Manager Deleted")


@adminRouter.get('/')
async def allAdmins(admin=Depends(getCurrentAdmin)):
    if admin.authority != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="request not Allowed")

    return AdminService.getAllAdmins()
