from django.contrib import admin
from .models import Matriculas,Consultor,cad_campanhas,cad_cursos,cad_polos,tipo_curso


# Register your models here.

class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('id','data_matricula', 'nome_aluno', 'numero_ra', 'curso', 'tipo_curso', 'campanha', 'create_date', 'update_date', 'active', 'processo_sel' )
    list_filter = ('nome_aluno', 'numero_ra', 'curso', 'tipo_curso', 'campanha', 'create_date', 'update_date', 'active') # Criar filtros

admin.site.register(Matriculas, MatriculasAdmin)


@admin.register(Consultor)
class ConsultorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')


@admin.register(cad_campanhas)
class cad_campanhasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'create_date', 'update_date', 'active')

@admin.register(cad_cursos)
class cad_cursosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'create_date', 'update_date', 'active')

@admin.register(cad_polos)
class cad_polosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'create_date', 'update_date', 'active')

@admin.register(tipo_curso)
class tipo_cursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'pontos', 'create_date', 'update_date', 'active')
