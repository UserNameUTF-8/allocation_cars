import uvicorn
from fastapi import FastAPI

from controllers.AdminController import adminRouter
from controllers.UserController import userRouter
from controllers.CarController import carRoute

app = FastAPI()

app.include_router(adminRouter, tags=['Admins'])
app.include_router(userRouter, tags=['Users'])
app.include_router(carRoute, tags=['Car'])
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
