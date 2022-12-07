import logging
import schema

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

from .. import bootstrap, views

app = FastAPI()

logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")


@app.get("/images")
async def get_all_images():
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
    request_dict = await request.json()

    try:
        bus.handle_message(
            "CreateImage",
            request_dict,
        )
    except schema.SchemaError as e:
        raise HTTPException(422, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(503, detail="Internal Server Error")

    response.status_code = 201
    return response


@app.get("/images/{uuid}")
async def get_image_meta_data_by_uuid(request: Request, response: Response, uuid: str):
    result = views.get_image_by_uuid(uuid=uuid, uow=bus.uow)

    if not result:
        raise HTTPException(404, detail="Item not found")

    return JSONResponse(content=result)


@app.post(
    "/images/{uuid}/metadata",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["label", "x_1", "y_1", "x_2", "y_2", "confidence"],
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "x_1": {"type": "number"},
                            "y_1": {"type": "number"},
                            "x_2": {"type": "number"},
                            "y_2": {"type": "number"},
                            "confidence": {"type": "number"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def add_metadata_to_image(request: Request, response: Response, uuid: str):
    request_dict = await request.json()
    request_dict.update({"image_uuid": uuid})

    try:
        bus.handle_message(
            "AddMetaDataToImage",
            request_dict,
        )
    except schema.SchemaError as e:
        raise HTTPException(422, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(503, detail="Internal Server Error")

    response.status_code = 201
    return response
