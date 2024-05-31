from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# Create your models here.

class Media(models.Model):
    file = models.FileField(upload_to='only_medias/',
                            verbose_name=_('File'),
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Medias')

    def __str__(self):
        return f"Id: {self.id}|Name: {self.file.name.split('/')[-1]}"

    # Валидация файлов по формату
    def clean(self):
        file_extension = self.file.name.split('.')[-1].lower()
        if file_extension not in ['jpg', 'jpeg', 'png', 'webp']:
            raise ValidationError(
                _(f"The file {self.file.name.split('/')[-1]} is not a valid image format. Allowed formats are JPG, JPEG, PNG, and WEBP."))

