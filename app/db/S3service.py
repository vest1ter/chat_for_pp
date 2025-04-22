import asyncio

from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from app.core.config import settings


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

    async def upload_file(
            self,
            file_path: str,
            object_name: str,
    ):
        object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )

async def main():
    s3_client = S3Client(
        root_user=settings.S3.root_user,
        root_password=settings.S3.root_password,
        endpoint_url=settings.S3.endpoint_url,
        bucket_name=settings.S3.bucket_name,
    )

    await s3_client.upload_file("vilka.png", "vilka.png")

if __name__ == "__main__":
    asyncio.run(main())