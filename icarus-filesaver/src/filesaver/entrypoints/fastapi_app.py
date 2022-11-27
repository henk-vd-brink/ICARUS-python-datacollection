import os
import logging
import schema

from fastapi import FastAPI, Request, Response, HTTPException, UploadFile
from fastapi.responses import FileResponse

from .. import config, bootstrap, domain

logger = logging.getLogger(__name__)


app = FastAPI()

BASE_FILE_PATH = config.get_base_file_path()

bootstrap_dict = bootstrap.bootstrap()

command_handlers = bootstrap_dict.get("command_handlers")


@app.get("/files/{file_name}")
def get_file_from_file_name(request: Request, response: Response, file_name: str):
    file_path = BASE_FILE_PATH / file_name

    if not os.path.exists(file_path):
        return HTTPException(404, detail="Requested Resource Does Not Exist")

    return FileResponse(file_path)


@app.post("/files")
async def upload_file(request: Request, response: Response, file: UploadFile = None):
    try:
        cmd = domain.commands.StoreFileOnFileSystem(
            file_name=file.filename, file_bytes=file.file
        )

        handler = command_handlers[type(cmd)]
        handler(cmd)
    except Exception as e:
        logger.exception(e)
        return HTTPException(500, detail="Internal Server Error")

    response.status_code = 204
    response.headers.update({"location": "/uploaded_images/" + file.filename})
    return response
