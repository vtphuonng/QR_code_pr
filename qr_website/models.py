from django.db import models

class ProfileImage(models.Model):
    image = models.FileField(upload_to='profile')

class records(models.Model):
    excel_id = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255)
    create_day = models.CharField(max_length=255)

    def __str__(self) -> str:
        return(f'{self.excel_id} {self.name} {self.create_day}')