import boto3
from botocore.config import Config

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.r2_endpoint_url,
    aws_access_key_id=settings.r2_access_key_id,
    aws_secret_access_key=settings.r2_secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)


def gerar_url_upload(chave: str, content_type: str, expira_em: int = 300) -> str:
    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.r2_bucket_name, "Key": chave, "ContentType": content_type},
        ExpiresIn=expira_em,
    )


def gerar_url_download(chave: str, expira_em: int = 300) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.r2_bucket_name, "Key": chave},
        ExpiresIn=expira_em,
    )


def excluir_arquivo(chave: str) -> None:
    s3_client.delete_object(Bucket=settings.r2_bucket_name, Key=chave)