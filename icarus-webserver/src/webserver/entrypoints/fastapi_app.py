import logging
import os
import schema

from fastapi import FastAPI, Request, Response, HTTPException, UploadFile

from fastapi.responses import JSONResponse, FileResponse

from .. import domain, bootstrap, views

app = FastAPI()

logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")


@app.get("/images", status_code=200)
async def get_all_images(
    request: Request,
    response: Response,
):
    results = views.get_all_images(bus.uow)
    return JSONResponse(content=results)


@app.post(
    "/images",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["image_uuid", "meta_data"],
                        "type": "object",
                        "properties": {
                            "image_uuid": {"type": "string"},
                            "meta_data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "label": {"type": "string"},
                                        "bx": {"type": "number"},
                                        "by": {"type": "number"},
                                        "w": {"type": "number"},
                                        "h": {"type": "number"},
                                    },
                                },
                            },
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_image(
    request: Request,
    response: Response,
):
    request_json = await request.json()

    try:
        bus.handle_message(
            "CreateImage",
            request_json,
        )
    except schema.SchemaError as e:
        return HTTPException(404, detail=str(e))

    response.status_code = 201
    return response


@app.get("/images/{uuid}", status_code=200)
async def get_image_meta_data_by_uuid(request: Request, response: Response, uuid: str):
    result = views.get_image_by_uuid(uuid=uuid, uow=bus.uow)

    if not result:
        return HTTPException(404, detail="Item not found")

    return JSONResponse(content=result)


@app.post(
    "/images/{uuid}/metadata",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["label", "bx", "by", "w", "h"],
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "bx": {"type": "number"},
                            "by": {"type": "number"},
                            "w": {"type": "number"},
                            "h": {"type": "number"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def add_metadata_to_image(request: Request, response: Response, uuid: str):
    request_json = await request.json()
    request_json.update({"image_uuid": uuid})

    try:
        bus.handle_message(
            "AddMetaDataToImage",
            request_json,
        )
    except schema.SchemaError as e:
        return HTTPException(404, detail=str(e))

    response.status_code = 201
    return response


@app.get("/files/{file_name}", status_code=200)
def get_image_file(request: Request, response: Response, file_name: str):
    base_file_path = "/usr/docker_user/data/"
    absolute_file_path = base_file_path + file_name

    if not os.path.exists(absolute_file_path):
        return HTTPException(404, detail="Requested resource does not exist")

    return FileResponse(base_file_path + file_name)


@app.post("/files", status_code=204)
async def upload_image_file(
    request: Request, response: Response, file: UploadFile = None
):
    try:
        bus.handle_message(
            "StoreImage",
            {"image_bytes": file.file, "file_name": file.filename},
        )
    except Exception as e:
        logger.exception(e)
        return HTTPException(404, detail=str(e))

    response.headers.update({"Location": "/uploaded_images/" + file.filename})
