import asyncio

from aiobotocore.session import get_session
from fastapi import UploadFile, HTTPException
from contextlib import asynccontextmanager
from app.core.config import settings
import logging


logger = logging.getLogger(__name__)


class S3Client:
    def __init__(self,
                 root_user: str,
                 root_password: str,
                 endpoint_url: str,
                 bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": root_user,
            "aws_secret_access_key": root_password,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client


    async def upload_fileobj(self, file_obj: UploadFile, object_name: str):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=await file_obj.read(),
                ContentType=file_obj.content_type
            )

    async def get_presigned_url(self, object_name: str, expires_in: int = 3600):
        try:
            async with self.get_client() as client:
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': object_name},
                    ExpiresIn=expires_in
                )
            return url
        except Exception as e:
            logger.error(f"Presigned URL error: {str(e)}")
            raise HTTPException(500, "Failed to generate URL")

    async def delete_file(self, object_name: str) -> bool:
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
            logger.info(f"File deleted: {object_name}")
            return True
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return False

    async def file_exists(self, object_name: str) -> bool:
        try:
            async with self.get_client() as client:
                await client.head_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
            return True
        except client.exceptions.NoSuchKey:
            return False
        except Exception as e:
            logger.error(f"Exists check error: {str(e)}")
            return False


s3_client = S3Client(
    root_user=settings.S3.root_user,
    root_password=settings.S3.root_password,
    endpoint_url=settings.S3.endpoint_url,
    bucket_name=settings.S3.bucket_name,
)

async def get_s3_client() -> S3Client:
    return s3_client



