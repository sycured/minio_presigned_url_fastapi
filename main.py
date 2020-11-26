#!/usr/bin/env python3
# coding: utf-8

"""Minio - Presigned URL webservice."""

from datetime import timedelta

from config import access_key, endpoint, secret_key, ssl

from const import download_responses, tags_metadata, upload_responses

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse, Response

from minio import Minio

from pydantic import BaseModel

tdelta_15m: timedelta = timedelta(minutes=15)

minio_client: Minio = Minio(endpoint=endpoint, access_key=access_key,
                            secret_key=secret_key, secure=ssl)

app: FastAPI = FastAPI(title='Minio - Presigned URL webservice',
                       docs_url='/', openapi_tags=tags_metadata)


class UploadReqJson(BaseModel):
    """Defines the JSON schema used by /upload."""

    bucket: str
    file: str


async def bucket_exists(name: str) -> bool:
    """Permit to know if the bucket exists."""
    return name in (i.name for i in minio_client.list_buckets())


async def file_exists(bucket: str, name: str) -> bool:
    """Permit to know if the file exists in the bucket."""
    return name in (i.object_name for i in
                    minio_client.list_objects(bucket_name=bucket,
                                              prefix=name[:5]))


async def return_code(http_code: int, status: str) -> Response:
    """Return a specific string or content with defined http code."""
    return JSONResponse(status_code=http_code, content=status)


@app.get('/download/{bucket}/{file}', tags=['download'],
         status_code=307, responses=download_responses)
async def download(bucket: str, file: str):
    """Obtain presigned url to download a file."""
    return await return_code(http_code=404,
                             status='bucket or file not found') if not (
            await bucket_exists(bucket) and await file_exists(bucket, file)
    ) else RedirectResponse(url=minio_client.presigned_get_object(
        bucket_name=bucket, object_name=file, expires=timedelta(minutes=15)
    ), status_code=307)


@app.post('/upload', tags=['upload'], responses=upload_responses)
async def upload(body: UploadReqJson):
    """Obtain presigned url to upload a file."""
    return await return_code(http_code=404, status=f'{body.bucket} not found'
                             ) if not await bucket_exists(
        name=body.bucket) else minio_client.presigned_put_object(
        bucket_name=body.bucket, object_name=body.file, expires=tdelta_15m)
