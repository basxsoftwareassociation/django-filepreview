import logging
import os
from functools import partialmethod

from preview_generator.manager import PreviewManager

from django.conf import settings
from django.db import models
from django.utils.html import mark_safe


def _tohtml(obj, previewfield):
    previewfile = getattr(obj, previewfield.name)
    originalfile = getattr(obj, previewfield.filefieldname)
    try:
        previewfile and previewfile.file and originalfile and originalfile.file
    except FileNotFoundError:
        return None
    if previewfile:
        return mark_safe(
            f'<a href="{originalfile.url}"><img src={previewfile.url} width="{previewfile.width}" height="{previewfile.height}"/></a>'
        )
    if originalfile:
        return mark_safe(
            f'<a href="{originalfile.url}"><i class="material-icons">open_in_browser</i></a>'
        )
    return None


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

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(
            cls,
            "get_%s_display" % self.name,
            partialmethod(_tohtml, previewfield=self),
        )

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
        if not getattr(model_instance, self.filefieldname):
            return ""
        try:
            return FilePreviewField.PREVIEW_MANAGER.get_jpeg_preview(
                getattr(model_instance, self.filefieldname).path,
                width=self.width,
                height=self.height,
            )[len(settings.MEDIA_ROOT) + 1 :]
        except Exception:
            logging.getLogger(__name__).exception(
                f"Error while generating file preview of {model_instance} on field {self.filefieldname}"
            )
            return ""
