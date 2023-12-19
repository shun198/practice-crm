from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from project.settings.environment import django_settings

if django_settings.DJANGO_SETTINGS_MODULE == "project.settings.local":
    storage_class = FileSystemStorage
else:
    storage_class = S3Boto3Storage


class CustomStorage(storage_class):
    file_overwrite = False
    counts = {}

    def get_alternative_name(self, file_root, file_ext):
        if file_root not in self.counts:
            self.counts[file_root] = 1
        new_file_name = (
            file_root + "_" + str(self.counts[file_root]) + file_ext
        )
        self.counts[file_root] += 1
        return new_file_name
