# FastAPI MinIO Image Uploader

This is a simple FastAPI application that allows users to upload images to a MinIO object storage server. The uploaded images are saved in a specified bucket on the MinIO server.

## Setup

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Set up your MinIO server and obtain the necessary credentials (URL, access key, secret key).
3. Create a `.env` file and set the following environment variables:
   ```
   BUCKET_NAME=<your_minio_bucket_name>
   MINIO_URL=<minio_server_url>
   MINIO_KEY=<minio_access_key>
   MINIO_SECRET=<minio_secret_key>
   MINIO_ROOT_USER=<minio_root_username>
   MINIO_ROOT_PASSWORD=<minio_root_password>
   ```
## Usage

1. Start the FastAPI application by running, for example `uvicorn main:app --reload`.
   optionally: use `docker-compose up` from repository, there is also `.env` file with dummy values.
2. Navigate to `http://localhost:8000/docs` to access the Swagger UI and interact with the API.
3. Use the `/images/` endpoint with a `POST` request to upload an image, for example:

```bash
curl -X 'POST' \
'http://localhost:8000/images/' \
-F 'file=@<image_path>;type=image/jpeg'
```

4. Use the `/images/{image_id}` endpoint with a `GET` request to download an image by providing its ID.

```bash
curl http://localhost:8000/images/afd52ea0-a46e-455a-9b6d-ea248fda22e8 --output <Image_name>
```

## Endpoints

### Upload Image

- **URL:** `/images/`
- **Method:** `POST`
- **Parameters:**
  - `file`: The image file to upload (multipart form-data).
- **Response:**
  - Status Code: 201 (Created) - Image uploaded successfully, UUID returned in the JSON ID field:
    ```
    {"message":"Image uploaded OK","ID":"afd52ea0-a46e-455a-9b6d-ea248fda22e8"}
    ```
  - Status Code: 400 (Bad Request) - Invalid image format.
  - Status Code: 500 (Internal Server Error) - Image upload failed.

- There is script that uploads all images from specified directory and generate CSV file with images path's and uploaded ID's
  For example, if you have started service with docker-compose you can run this script with sample_images by following command
  ```bash
  python3 upload_images.py --image_dir "sample_images" --csv_name "uploaded.csv" --csv_delimiter ";" --api_url "http://0.0.0.0:8000/images"
  ```

### Download Image

- **URL:** `/images/{image_id}`
- **Method:** `GET`
- **Parameters:**
  - `image_id`: The ID of the image to download.
- **Response:**
  - Status Code: 200 (OK) - Image retrieved successfully.
  - Status Code: 404 (Not Found) - Image not found.
  - Status Code: 500 (Internal Server Error) - Failed to retrieve the image.

### Delete Image

- **URL:** `/images/{image_id}`
- **Method:** `DELETE`
- **Parameters:**
  - `image_id`: The ID of the image to delete.
- **Response:**
  - Status Code: 200 (OK) - Image deleted successfully.
  - Status Code: 404 (Not Found) - Image not found.

## Notes

- Supported image formats: JPEG, PNG, GIF.
- The MinIO server must be accessible and properly configured for the application to function correctly.
- The application uses environment variables to securely store MinIO credentials and bucket information. Make sure to handle the production environment configurations securely (e.g., using environment variables).