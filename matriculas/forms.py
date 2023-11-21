from django import forms
from django.forms import ModelForm
from .models import Matriculas, Consultor, cad_campanhas, cad_cursos, cad_polos, tipo_curso
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

NUMERO_CONCURSO_CHOICES = (
    (51, '51'),
    (52, '52'),
    (53, '53'),
    (54, '54'),

)

class MatriculasForm(forms.ModelForm):
    numero_concurso = forms.CharField(widget=forms.Select(choices=NUMERO_CONCURSO_CHOICES))
    ano_concurso = forms.IntegerField()
    data_matricula = forms.DateTimeField()
    nome_aluno = forms.CharField()
    numero_ra = forms.CharField(label='RA', required=False)
    curso = forms.ModelChoiceField(queryset=cad_cursos.objects.all())
    tipo_curso = forms.ModelChoiceField(queryset=tipo_curso.objects.all())
    campanha = forms.ModelChoiceField(queryset=cad_campanhas.objects.all()) 
    valor_mensalidade = forms.DecimalField()
    desconto_polo = forms.DecimalField()
    desconto_total = forms.DecimalField()


    class Meta:
        model = Matriculas
        fields = (
            'numero_concurso',
            'ano_concurso',
            'data_matricula',
            'nome_aluno',
            'numero_ra',
            'curso',
            'tipo_curso',
            'campanha',
            'valor_mensalidade',
            'desconto_polo',
            'desconto_total',

        )
        
class ConsultorForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    birth_date = forms.DateField(widget=DateInput())
    area_code = forms.RegexField(
        label='DDD',
        regex=r"^\+?1?[0-9]{2}",
        error_messages={'invalid': 'DDD inválido.'},
    )
    phone_number = forms.RegexField(
        label='Telefone',
        regex=r"^\+?1?[0-9]{8,15}",
        error_messages={'invalid': 'Telefone inválido.'},
        
    )
    active = forms.BooleanField()
    class Meta:
        model = Consultor
        fields = (
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'area_code',
            'phone_number',
            'active',
        )


ESTADOS_UF = (
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
)




class PoloForm(forms.ModelForm):
    nome = forms.CharField()
    estado = forms.CharField(widget=forms.Select(choices=ESTADOS_UF))
    active = forms.BooleanField()
    
    
    class Meta:
        model = cad_polos
        fields = (
            'nome',
            'estado',
            'active',
        )
        
class CursosForm(forms.ModelForm):
    nome = forms.CharField()
    active = forms.BooleanField()
    
    class Meta:
        model = cad_cursos
        fields = (
            'nome',
            'active',
        )


class TipoCursoForm(forms.ModelForm):
    nome = forms.CharField()
    pontos = forms.IntegerField()
 
    
    class Meta:
        model = tipo_curso
        fields = (
            'nome',
            'pontos',
        )
        

class CampanhaForm(forms.ModelForm):
    nome = forms.CharField()
    active = forms.BooleanField()
    
    class Meta:
        model = cad_campanhas
        fields = (
            'nome',
            'active',
        )
        
class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
    
    def get_absolute_url(self):
        return reverse("matriculas:user_update", kwargs={'id': self.id}) #Direciona para a url de edição