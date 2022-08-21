from fastapi import FastAPI, Request, Response, HTTPException, UploadFile

app = FastAPI()


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
