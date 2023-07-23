import io
import logging
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from app.storage import MinioService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
minio = MinioService.get_instance()

router = APIRouter()


@router.post("/images/")
async def upload_file(file: UploadFile = File(None)) -> JSONResponse:
    if file:
        try:
            image_id = await minio.put_object(file)
            return JSONResponse(status_code=201, content={"message": "Image Uploaded OK", "ID": image_id})
        except:
            return JSONResponse(status_code=500, content={"error": "Something went wrong"})
    return JSONResponse(status_code=422, content={"error": "No file provided"})


@router.get("/images/{image_id}")
async def download(image_id: str):
    try:
        image_data = await minio.get_object(image_id)
        return StreamingResponse(io.BytesIO(image_data), media_type="image/jpg")
    except:
        return JSONResponse(status_code=404, content={"message": "Image not found"})


@router.delete("/images/{image_id}")
async def delete(image_id: str):
    try:
        await minio.remove_object(image_id)
    except:
        return JSONResponse(status_code=404, content={"message": "Image not found"})
