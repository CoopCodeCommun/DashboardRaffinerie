from django.db import models
from uuid import uuid4
# Create your models here.
from stdimage import JPEGField
from stdimage.validators import MinSizeValidator


class Contact(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    # L'email est obligatoire
    email = models.EmailField(max_length=100)

    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    structure = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)

    # Une image qui sera automatiquement convertie en JPG
    # avec la création de deux variations : 960x540 et un carré 270x270
    image = JPEGField(upload_to='images/',
                      validators=[MinSizeValidator(960, 540)],
                      variations={
                          'med': (960, 540),
                          'thumb': (270, 270, True)
                      },
                      delete_orphans=True,
                      verbose_name="Image du contact",
                      blank=True, null=True,
                      )

    # Une relation avec le modèle utilisateur.
    # Une fiche de contact peut être liée a un user
    user = models.ForeignKey('dashboard_user.CustomUser',
                             on_delete=models.PROTECT,
                             null=True, blank=True)
