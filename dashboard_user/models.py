from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from stdimage import StdImageField, JPEGField
from stdimage.validators import MinSizeValidator


class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)

    picture = JPEGField(upload_to='images/',
                          validators=[MinSizeValidator(720, 720)],
                          blank=True, null=True,
                          variations={
                              'hdr': (720, 720),
                              'med_crop': (540, 540, True),
                              'sm_crop': (270, 270, True)
                          },
                          delete_orphans=True,
                          verbose_name="picture",
                          )