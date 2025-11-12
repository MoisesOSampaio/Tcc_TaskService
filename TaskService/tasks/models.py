from django.db import models
from django.contrib.postgres.fields import ArrayField
class Task(models.Model):

    id_user = models.UUIDField(null=True, blank=True)
    titulo = models.TextField(max_length=150)
    descricao = models.TextField()
    skills = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list,
        help_text="Lista de habilidades necessárias para executar a tarefa"
    )
    prazo = models.DateField(null=True,blank=True)
    status = models.TextField(max_length=50)
    
    def __str__(self):
        return f"Task: {self.titulo}"


