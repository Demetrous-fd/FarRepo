from fastapi.responses import JSONResponse
from fastapi import APIRouter, status

from app import tasks


route = APIRouter(prefix="/tasks", tags=["Tasks"])


@route.get("/update_farpost_data")
async def update_farpost_data():
    task = tasks.update_farpost_data.delay()
    return JSONResponse(
        content={"task_id": task.id}, 
        status_code=status.HTTP_202_ACCEPTED
    )
