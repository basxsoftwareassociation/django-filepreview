import os

from django.conf import settings
from django.db import models

from preview_generator.manager import PreviewManager


class FilePreviewField(models.ImageField):
    PREVIEW_MANAGER = PreviewManager(
        os.path.join(settings.MEDIA_ROOT, "filepreviews"), create_folder=True
    )

    def __init__(self, filefieldname, width=200, height=200, **kwargs):
        kwargs["editable"] = False
        kwargs["default"] = ""
        self.filefieldname = filefieldname
        self.width = width
        self.height = height
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args = [self.filefieldname] + args
        kwargs["width"] = self.width
        kwargs["height"] = self.height
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        setattr(model_instance, self.attname, self._generate_preview(model_instance))
        return super().pre_save(model_instance, add)

    def _generate_preview(self, model_instance):
        return FilePreviewField.PREVIEW_MANAGER.get_jpeg_preview(
            getattr(model_instance, self.filefieldname).path,
            width=self.width,
            height=self.heighth,
        )[len(settings.MEDIA_ROOT) + 1 :]
