from src.storage.s3 import S3Client


class Storage:    
    def __new__(cls, storage_type):
        if storage_type == 'S3':
            return S3Client()
        else:
            raise NotImplementedError('Unsupported storage type')



