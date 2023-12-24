from django.utils.translation import gettext_lazy as _
from rest_framework.fields import FileField

from project.settings.base import MAX_FILE_SIZE_LIMIT


def upload_file_to_internal_value(self, data):
    try:
        file_name = data.name
        file_size = data.size
    except AttributeError:
        self.fail("invalid")

    if not file_name:
        self.fail("no_name")
    if not self.allow_empty_file and not file_size:
        self.fail("empty")
    if self.max_length and len(file_name) > self.max_length:
        self.fail(
            "max_length", max_length=self.max_length, length=len(file_name)
        )
    if file_size > MAX_FILE_SIZE_LIMIT:
        self.fail("file_size_over", max_size=MAX_FILE_SIZE_LIMIT / 1000000)
    return file_name


class CustomFileField(FileField):
    default_error_messages = {
        "required": _("No file was submitted."),
        "invalid": "無効なファイル形式です。指定されたファイル形式を使用してください",
        "no_name": _("No filename could be determined."),
        "empty": _("The submitted file is empty."),
        "max_length": _(
            "Ensure this filename has at most {max_length} characters (it has {length})."
        ),
        "file_size_over": "{max_size}MB 以下のファイルを登録してください",
    }

    def to_internal_value(self, data):
        file_name = upload_file_to_internal_value(self, data)
        if not file_name.lower().endswith(".pdf"):
            self.fail("invalid")
        return data
