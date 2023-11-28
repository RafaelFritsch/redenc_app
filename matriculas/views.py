from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count, Sum, Avg
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django import forms
from django.db.models.functions import TruncMonth
import os
from django.http import FileResponse
from django.http import JsonResponse




# Create your views here.

#LIST VIEWS ######################################################

class MatriculasListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/matriculas_list.html'
    login_url = 'login'
    paginate_by = 10
    model = Matriculas
    def get_queryset(self):
        
        name = self.request.GET.get("name")
        if name:
            object_list = self.model.objects.filter(nome_aluno__icontains=name).filter(usuario=self.request.user).order_by('-data_matricula') # Vizualiza somente os registros que o user criou
        else:
            object_list = self.model.objects.all().filter(usuario=self.request.user).order_by('-data_matricula') # Vizualiza somente os registros que o user criou
        return object_list
    
    
class MatriculaFileView(View):
    model = Matriculas

    def get(self, request, pk, *args, **kwargs):
        matricula = get_object_or_404(self.model, pk=pk)
        file_path = matricula.arquivos.path

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
                return response
        else:
            raise Http404
    

## Listar Users 

class UserListView(ListView):
    template_name = 'matriculas/user_list.html'
    model = User
    queryset = User.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adiciona os polos associados a cada usuário ao contexto
        context['polos'] = cad_polos.objects.filter(users__in=context['user_list'])

        return context
    
    


class CampanhaListView(ListView):
    template_name = 'matriculas/campanha_list.html'
    model = cad_campanhas
    queryset = cad_campanhas.objects.all()

class CursoListView(ListView):
    template_name = 'matriculas/curso_list.html'
    model = cad_cursos
    queryset = cad_cursos.objects.all()
    
class PoloListView(ListView):
    template_name = 'matriculas/polo_list.html'
    model = cad_polos
    queryset = cad_polos.objects.all()
    
class TipoCursoListView(ListView):
    template_name = 'matriculas/tipo_curso_list.html'
    model = tipo_curso
    queryset = tipo_curso.objects.all()
    
class ProcessoListView(ListView):
    template_name = 'matriculas/processo_list.html'
    model = cad_processo
    queryset = cad_processo.objects.all()


#NEW VIEWS ######################################################

class MatriculasNewView(LoginRequiredMixin,CreateView):  # Criar novo registro
    template_name = 'matriculas/matriculas_new.html'
    form_class = MatriculasForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  # TODO:  AJUSTAR NÃO ESTÁ FILTRANDO O CURSO POR TIPO
        return render(request, self.template_name, {'form': form})
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:matriculas_list')
    
# class UserNewView(CreateView):
#     template_name = 'matriculas/user_new.html'
#     form_class = UserForm

#     def form_valid(self, form):
#          return super().form_valid(form)
    
#     def get_success_url(self) -> str:
#         return reverse('matriculas:user_list')

class UserNewView(CreateView):
    template_name = 'matriculas/user_new.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)

        # Obtenha a instância do usuário recém-criado
        user_instance = form.instance

        # Adicione o código para vincular o usuário ao polo aqui
        # Supondo que você tenha um campo 'polo' no seu formulário
        selected_polo = form.cleaned_data['polo']

        if selected_polo:
            user_profile = UserProfile.objects.create(user=user_instance, polo=selected_polo)
            user_profile.save()

        return response

    def get_success_url(self) -> str:
        return reverse('matriculas:user_list')




    
class PoloNewView(CreateView):
    template_name = 'matriculas/polo_new.html'
    form_class = PoloForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:polo_list')


class CursosNewView(CreateView):
    template_name = 'matriculas/cursos_new.html'
    form_class = CursosForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:curso_list')
    
class TipoCursoNewView(CreateView):
    template_name = 'matriculas/tipo_curso_new.html'
    form_class = TipoCursoForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:tipo_curso_list')
    
class CampanhaNewView(CreateView):
    template_name = 'matriculas/campanha_new.html'
    form_class = CampanhaForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:campanha_list')   
    
class ProcessoNewView(CreateView):
    template_name = 'matriculas/processo_new.html'
    form_class = ProcessoForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:processo_list')
    

    
    
#UPDATE VIEWS ######################################################
    
class MatriculasUpdateView(UpdateView):
    template_name = 'matriculas/matriculas_new.html'
    form_class = MatriculasForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Matriculas, id=id)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:matriculas_list')  #Quando finalizar a ação com sucesso retorna para tela anterior da lista

class UserUpdateView(UpdateView):
    template_name = 'matriculas/consultor_new.html'
    form_class = UserForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(User, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:user_list')
    
class ConsultorUpdateView(UpdateView):
    template_name = 'matriculas/consultor_new.html'
    form_class = ConsultorForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Consultor, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:consultor_list')
    
class CampanhaUpdateView(UpdateView):
    template_name = 'matriculas/campanha_new.html'
    form_class = CampanhaForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_campanhas, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:campanha_list')

class CursoUpdateView(UpdateView):
    template_name = 'matriculas/cursos_new.html'
    form_class = CursosForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_cursos, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:curso_list')
    
class TipoCursoUpdateView(UpdateView):
    template_name = 'matriculas/tipo_curso_new.html'
    form_class = TipoCursoForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(tipo_curso, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:tipo_curso_list')
    
class PoloUpdateView(UpdateView):
    template_name = 'matriculas/polo_new.html'
    form_class = PoloForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_polos, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:polo_list')
    
    
class ProcessoUpdateView(UpdateView):
    template_name = 'matriculas/processo_new.html'
    form_class = ProcessoForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_processo, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:processo_list')
    

# DELETE VIEWS ######################################################

class MatriculasDeleteView(DeleteView): 
    model = Matriculas
    template_name = 'matriculas/matriculas_delete.html'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Matriculas, id=id)

    def get_success_url(self):
        success_url = reverse('matriculas:matriculas_list')
        return success_url

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Verifica se o arquivo deve ser excluído
        excluir_arquivo = request.POST.get('excluir_arquivo')
        print(f"Excluir arquivo: {excluir_arquivo}")

        # Verifica se o valor de excluir_arquivo é 'True' (uma string)
        if excluir_arquivo == 'True' and self.object.comprovante:
            print("Excluindo arquivo...")
            print(f"Caminho do arquivo: {self.object.comprovante.path}")
            self.object.comprovante.delete()

        # Chama o método delete da superclasse
        response = super().delete(request, *args, **kwargs)

        # Retorna a URL de sucesso
        return response







# class MatriculasDeleteView(DeleteView):
#     def get_object(self):
#         id = self.kwargs.get('id')
#         return get_object_or_404(Matriculas, id=id)
    
#     def get_success_url(self):
#         return reverse('matriculas:matriculas_list') 
    
#     def delete(self, request, *args, **kwargs):
#         # Chama o método get_success_url antes de excluir o objeto
#         success_url = self.get_success_url()

#         # Obtém a instância da matrícula
#         matricula = self.get_object()

#         # Verifica se o arquivo deve ser excluído
#         excluir_arquivo = request.POST.get('excluir_arquivo')
#         if excluir_arquivo == 'True' and matricula.comprovante:
#             matricula.comprovante.delete()

#         # Chama o método delete da superclasse
#         response = super().delete(request, *args, **kwargs)

#         # Retorna a URL de sucesso
#         return response


class ConsultorDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Consultor, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:consultor_list')
    
    
class CampanhaDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_campanhas, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:campanha_list')
    
class CursoDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_cursos, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:curso_list')
    
    
class TipoCursoDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(tipo_curso, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:tipo_curso_list')
    
class PoloDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_polos, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:polo_list')
    
class ProcessoDeleteView(DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_processo, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:processo_list')


## Consultas

        

def RankView(request):
    context = {}
    context['usuarios'] = User.objects.all()
    
    context['contagem_matriculas'] = []
    for usuario in context['usuarios']:
        contagem = Matriculas.objects.filter(usuario=usuario).count()
        
        soma_pontos = tipo_curso.objects.filter(matriculas__usuario=usuario).aggregate(soma_pontos=models.Sum('pontos'))['soma_pontos']
        
    # Calcula a data da última matrícula do usuário
        ultima_matricula = Matriculas.objects.filter(usuario=usuario).order_by('-create_date').first()
        
        # Calcula a diferença de dias entre a última matrícula e a data atual
        if ultima_matricula:
            agora = datetime.now(ultima_matricula.create_date.tzinfo)
            dias_sem_matricula = (agora - ultima_matricula.create_date).days
        else:
            dias_sem_matricula = None
            
        
        # Adiciona um novo campo 'cor' ao dicionário
        if dias_sem_matricula is not None:
            if dias_sem_matricula <= 1:
                cor = 'verde'
            elif dias_sem_matricula <= 3:
                cor = 'amarela'
            else:
                cor = 'vermelha'
        else:
            cor = 'nunca'
            
        context['contagem_matriculas'].append({
            'usuario': usuario.username, 
            'contagem': contagem,
            'soma_pontos': soma_pontos if soma_pontos is not None else 0, # Garante que a soma seja 0 se não houver pontos
            'dias_sem_matricula': dias_sem_matricula,
            'cor': cor })  
        
        # Ordena a lista de dicionários com base na chave 'contagem'
        context['contagem_matriculas'].sort(key=lambda x: x['contagem'], reverse=True)        

        # Antes de renderizar o template, adicione o número total de linhas ao contexto
        context['num_linhas'] = range(1, len(context['contagem_matriculas']) + 1)

    return render(request, 'matriculas/consulta.html', context)



