from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
import django_filters
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Consultor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    birth_date = models.DateField()
    area_code = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=9)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'consultor'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"  
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def get_data_nascimento(self):
        return self.birth_date.strftime('%d/%m/%Y')
    def get_data_create(self):
        return self.create_date.strftime('%d/%m/%Y')
    def get_data_update(self):
        return self.update_date.strftime('%d/%m/%Y')
    def get_full_phone(self):
        return f"({self.area_code}) {self.phone_number}"
    def get_absolute_url(self):
        return reverse("matriculas:consultor_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:consultor_delete", kwargs={'id': self.id})# Exclui o resgistro


class cad_polos(models.Model):
    ESTADOS_UF = [
        ('AC', 'ACRE'),
        ('AL', 'ALAGOAS'),
        ('AP', 'AMAPÁ'),
        ('AM', 'AMAZONAS'),
        ('BA', 'BAHIA'),
        ('CE', 'CEARÁ'),
        ('DF', 'DISTRITO FEDERAL'),
        ('ES', 'ESPÍRITO SANTO'),
        ('GO', 'GOIÁS'),
        ('MA', 'MARANHÃO'),
        ('MT', 'MATO GROSSO'),
        ('MS', 'MATO GROSSO DO SUL'),
        ('MG', 'MINAS GERAIS'),
        ('PA', 'PARÁ'),
        ('PB', 'PARAÍBA'),
        ('PR', 'PARANÁ'),
        ('PE', 'PERNAMBUCO'),
        ('PI', 'PIAUÍ'),
        ('RJ', 'RIO DE JANEIRO'),
        ('RN', 'RIO GRANDE DO NORTE'),
        ('RS', 'RIO GRANDE DO SUL'),
        ('RO', 'RONDÔNIA'),
        ('RR', 'RORAIMA'),
        ('SC', 'SANTA CATARINA'),
        ('SP', 'SÃO PAULO'),
        ('SE', 'SERGIPE'),
        ('TO', 'TOCANTINS')
    ]
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADOS_UF)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
        # Relação ManyToManyField com o modelUser
    
    
    class Meta:
        db_table = 'polos'
        
    def __str__(self):
        return self.nome
    
    def get_nome_polo(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("matriculas:polo_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:polo_delete", kwargs={'id': self.id})# Exclui o resgistro

class cad_cursos(models.Model):
    nome = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cursos'
        
    def __str__(self):
        return self.nome
    
    def get_data_create_curso(self):
        return self.create_date.strftime('%d/%m/%Y')
    
    def get_data_update_curso(self):
        return self.update_date.strftime('%d/%m/%Y')
    
    def get_absolute_url(self):
        return reverse("matriculas:curso_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:curso_delete", kwargs={'id': self.id})# Exclui o resgistro

class cad_campanhas(models.Model):
    nome = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'campanhas'
        
    def __str__(self):
        return self.nome
    
    def get_data_create_camp(self):
        return self.create_date.strftime('%d/%m/%Y')
    
    def get_data_update_camp(self):
        return self.update_date.strftime('%d/%m/%Y')
    
    def get_absolute_url(self):
        return reverse("matriculas:campanha_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:campanha_delete", kwargs={'id': self.id})# Exclui o resgistro
    
class tipo_curso(models.Model):
    nome = models.CharField(max_length=100)
    pontos = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tipo_curso'
        
    def __str__(self):
        return self.nome
    
    def get_data_create_tp(self):
        return self.create_date.strftime('%d/%m/%Y')
    
    def get_data_update_tp(self):
        return self.update_date.strftime('%d/%m/%Y')
    
    def get_absolute_url(self):
        return reverse("matriculas:tipo_curso_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:tipo_curso_delete", kwargs={'id': self.id})# Exclui o resgistro



NUMERO_CONCURSO_CHOICES = (
    (51, '51'),
    (52, '52'),
    (53, '53'),
    (54, '54'),

)

class Matriculas(models.Model):
    id = models.AutoField(primary_key=True)
    numero_concurso = models.IntegerField(null=True, choices=NUMERO_CONCURSO_CHOICES)
    ano_concurso = models.IntegerField(null=True)
    data_matricula = models.DateTimeField()
    nome_aluno = models.CharField(max_length=200)
    numero_ra = models.CharField(max_length=12)
    curso = models.ForeignKey(cad_cursos, on_delete=models.CASCADE)
    tipo_curso = models.ForeignKey(tipo_curso, on_delete=models.CASCADE)
    campanha = models.ForeignKey(cad_campanhas, on_delete=models.CASCADE) 
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    desconto_polo = models.DecimalField(max_digits=4, decimal_places=2)
    desconto_total = models.DecimalField(max_digits=4, decimal_places=2)
    pontos_trocados = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    comprovante = models.ImageField(upload_to='comprovantes/', blank=True, null=True)
    active = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
   
   
    
    class Meta:
        db_table = 'matricula'
        
    def __str__(self):
        return self.nome_aluno
    
    def get_data_matricula(self):
        return self.data_matricula.strftime('%d/%m/%Y')
    
    def get_absolute_url(self):
        return reverse("matriculas:matriculas_update", kwargs={'id': self.id}) #Direciona para a url de edição
    
    def get_delete_url(self):
        return reverse("matriculas:matriculas_delete", kwargs={'id': self.id})# Exclui o resgistro
    

""" class CustomUser(AbstractUser):
    # Adicione seus campos personalizados aqui
    polo = models.ManyToManyField(cad_polos, blank=True)
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # Adicione outros campos conforme necessário

    def __str__(self):
        return self.username """