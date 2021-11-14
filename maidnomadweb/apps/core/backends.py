from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False  # 同名ファイルは上書きせずに似た名前のファイルに
