from fastapi import FastAPI, Request, Response, HTTPException, UploadFile

from .. import bootstrap, config, domain


app = FastAPI()

bootstrap_dict = bootstrap.bootstrap()

command_handlers = bootstrap_dict.get("command_handlers")


@app.post("/files", status_code=204)
async def upload_image_file(
    request: Request, response: Response, file: UploadFile = None
):
    try:
        cmd = domain.commands.StoreFileOnFileSystem(
            file_name=file.filename, file_bytes=file.file
        )

        handler = command_handlers[type(cmd)]
        handler(cmd)
    except Exception as e:
        print(e)

    response.headers.update({"Location": "/uploaded_images/" + file.filename})
