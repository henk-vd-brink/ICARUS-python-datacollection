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
        cmd = domain.commands.StoreFile(file_name=file.filename, file=file.file)

        handler = command_handlers[cmd]
        handler(cmd)
    except Exception:
        pass

    response.headers.update({"Location": "/uploaded_images/" + file.filename})
