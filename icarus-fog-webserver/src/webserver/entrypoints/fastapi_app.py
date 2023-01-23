import logging
import schema
import os

from fastapi import FastAPI, Request, Response, HTTPException, UploadFile
from fastapi.responses import JSONResponse, FileResponse

from .. import bootstrap, views

app = FastAPI()

logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")


@app.get("/images")
async def get_all_images():
    results = views.get_all_images(bus.uow)
    return JSONResponse(content=results)


@app.get("/images/{uuid}")
async def get_image_meta_data_by_uuid(uuid: str):
    result = views.get_image_by_uuid(uuid=uuid, uow=bus.uow)

    if not result:
        raise HTTPException(404, detail="Item not found")

    return JSONResponse(content=result)


@app.post("/uploaded_images")
async def upload_image(response: Response, file: UploadFile = None):
    try:
        bus.handle_message(
            "StoreUploadedImage", {"file_bytes": file.file, "file_name": file.filename}
        )
    except schema.SchemaError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AttributeError as e:
        logger.exception(e)
        raise HTTPException(401, detail="Bad Request")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    response.headers.update({"Location": "/uploaded_images/" + file.filename})
    response.status_code = 201
    return response


@app.get("/uploaded_images/{file_name}")
async def get_uploaded_image_from_file_name(file_name):
    base_file_path = "/home/docker_user/data/"
    absolute_file_path = base_file_path + file_name

    if not os.path.exists(absolute_file_path):
        return HTTPException(404, detail="Bad Request")

    return FileResponse(absolute_file_path)


if __name__ == "__main__":
    pass
else:
    gunicorn_logger = logging.getLogger("gunicorn.info")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
