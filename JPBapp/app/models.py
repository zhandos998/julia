from django.db import models


# Create your models here.
class Variable(models.Model):
    name = models.CharField(primary_key=True, max_length=100, verbose_name='Переменная')
    description = models.TextField(verbose_name='Значение')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Переменная'
        verbose_name_plural = 'Переменные'