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
from django.contrib.auth.models import Group, Permission



#LIST VIEWS ######################################################
# 
def lista_processos(request):
    # Filtra os processos ativos
    processos_ativos = cad_processo.objects.filter(ativo=True)
    # Passa a lista filtrada para o template
    return render (request, 'matriculas/processo_ativo.html', {'processos': processos_ativos})  




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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtém o processo ativo
        processo_ativo = cad_processo.objects.filter(ativo=True).first()

        # Adiciona o objeto processo_ativo ao contexto
        context['cad_processo'] = processo_ativo

        return context

    
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

class UserListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/user_list.html'
    model = User
    queryset = User.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adiciona os polos associados a cada usuário ao contexto
        context['polos'] = cad_polos.objects.filter(users__in=context['user_list'])
        
        # Adiciona os cargos de cada usuário ao contexto
        user_profiles = UserProfile.objects.filter(user__in=context['user_list'])
        context['cargos'] = {profile.user_id: profile.cargo for profile in user_profiles}

        return context
    
    


class CampanhaListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/campanha_list.html'
    model = cad_campanhas
    queryset = cad_campanhas.objects.all()

class CursoListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/curso_list.html'
    model = cad_cursos
    queryset = cad_cursos.objects.all()
    
class PoloListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/polo_list.html'
    model = cad_polos
    queryset = cad_polos.objects.all()
    
class TipoCursoListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/tipo_curso_list.html'
    model = tipo_curso
    queryset = tipo_curso.objects.all()
    
class ProcessoListView(LoginRequiredMixin, ListView):
    template_name = 'matriculas/processo_list.html'
    model = cad_processo
    queryset = cad_processo.objects.all()


    



#NEW VIEWS ######################################################

class MatriculasNewView(LoginRequiredMixin,CreateView):  # Criar novo registro
    template_name = 'matriculas/matriculas_new.html'
    form_class = MatriculasForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  
        return render(request, self.template_name, {'form': form})
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        # Obtém o objeto tipo_curso a partir do ID
        tipo_curso_id = form.cleaned_data['tipo_curso'].id

        tipo_curso_obj = get_object_or_404(tipo_curso, id=tipo_curso_id)
        
        # Atribui o objeto tipo_curso ao campo no modelo
        form.instance.tipo_curso = tipo_curso_obj

        # Atribui o objeto curso ao campo no modelo
        form.instance.curso = form.cleaned_data['curso']

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('matriculas:matriculas_list')
    

    
def get_cursos(request):
    tipo_curso_id = request.GET.get('tipo_curso')
    cursos = cad_cursos.objects.filter(tipo_curso_id=tipo_curso_id).values('id', 'nome')
    cursos_list = list(cursos)
    print(cursos_list)
    return JsonResponse(cursos_list, safe=False)

   

class UserNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/user_new.html'
    form_class = UserForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user_instance = form.instance
        selected_polo = form.cleaned_data['polo']
        selected_cargo = form.cleaned_data['cargo'] 
        
        # Se o cargo for 'USUARIO', adicione as permissões necessárias
        if selected_cargo == 'U':
            # Associe o usuário ao grupo 'UsuarioGroup' (crie o grupo se necessário)
            usuario_group, created = Group.objects.get_or_create(name='UsuarioGroup')
            user_instance.groups.add(usuario_group)


        if selected_polo:
            user_profile = UserProfile.objects.create(user=user_instance, polo=selected_polo, cargo=selected_cargo)
            user_profile.save()

        return response

    def get_success_url(self) -> str:
        return reverse('matriculas:user_list')




    
class PoloNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/polo_new.html'
    form_class = PoloForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:polo_list')


class CursosNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/cursos_new.html'
    form_class = CursosForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:curso_list')
    
class TipoCursoNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/tipo_curso_new.html'
    form_class = TipoCursoForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:tipo_curso_list')
    
class CampanhaNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/campanha_new.html'
    form_class = CampanhaForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:campanha_list')   
    
class ProcessoNewView(LoginRequiredMixin, CreateView):
    template_name = 'matriculas/processo_new.html'
    form_class = ProcessoForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('matriculas:processo_list')
    

    
    
#UPDATE VIEWS ######################################################
    
class MatriculasUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'matriculas/matriculas_update.html'
    form_class = MatriculasForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Matriculas, id=id)

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)

        # Preenche os campos 'tipo_curso' e 'curso' com os valores atuais
        matricula = self.get_object()
        form.fields['tipo_curso'].initial = matricula.tipo_curso.id if matricula.tipo_curso else None
        form.fields['curso'].initial = matricula.curso.id if matricula.curso else None

        return form
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:matriculas_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'matriculas/consultor_new.html'
    form_class = UserForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(User, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:user_list')
    
# class ConsultorUpdateView(LoginRequiredMixin, UpdateView):
#     template_name = 'matriculas/consultor_new.html'
#     form_class = ConsultorForm
    
#     def get_object(self):
#         id = self.kwargs.get('id')
#         return get_object_or_404(Consultor, id=id)  # Retorna o objeto consultor a partir do id
    
#     def form_valid(self, form):
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('matriculas:consultor_list')
    
class CampanhaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'matriculas/campanha_new.html'
    form_class = CampanhaForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_campanhas, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:campanha_list')

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'matriculas/cursos_new.html'
    form_class = CursosForm
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_cursos, id=id)  # Retorna o objeto consultor a partir do id
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('matriculas:curso_list')
    
class TipoCursoUpdateView(LoginRequiredMixin, UpdateView):
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
    
    
class ProcessoUpdateView(LoginRequiredMixin, UpdateView):
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

class MatriculasDeleteView(LoginRequiredMixin, DeleteView): 
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


# class ConsultorDeleteView(LoginRequiredMixin, DeleteView):
#     def get_object(self):
#         id = self.kwargs.get('id')
#         return get_object_or_404(Consultor, id=id)
    
#     def get_success_url(self):
#         return reverse('matriculas:consultor_list')
    
    
class CampanhaDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_campanhas, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:campanha_list')
    
class CursoDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_cursos, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:curso_list')
    
    
class TipoCursoDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(tipo_curso, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:tipo_curso_list')
    
class PoloDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_polos, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:polo_list')
    
class ProcessoDeleteView(LoginRequiredMixin, DeleteView):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(cad_processo, id=id)
    
    def get_success_url(self):
        return reverse('matriculas:processo_list')


## Consultas

        

""" def RankView(request):     #Funcional caso não funcione retornar
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
 """

from datetime import datetime
from django.shortcuts import render
from .models import User, Matriculas, tipo_curso, cad_campanhas

def RankView(request):
    context = {}
    context['usuarios'] = User.objects.all()

    # Obtém a campanha ativa
    processo_ativo = cad_processo.objects.filter(ativo=True).first()

    if processo_ativo:
        data_inicio = processo_ativo.data_inicial_processo
        data_fim = processo_ativo.data_final_processo

        context['contagem_matriculas'] = []

        for usuario in context['usuarios']:
            contagem = Matriculas.objects.filter(usuario=usuario, create_date__range=[data_inicio, data_fim]).count()

            soma_pontos = tipo_curso.objects.filter(matriculas__usuario=usuario).aggregate(soma_pontos=models.Sum('pontos'))['soma_pontos']

            ultima_matricula = Matriculas.objects.filter(usuario=usuario).order_by('-create_date').first()

            if ultima_matricula:
                agora = datetime.now(ultima_matricula.create_date.tzinfo)
                dias_sem_matricula = (agora - ultima_matricula.create_date).days
            else:
                dias_sem_matricula = None

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
                'soma_pontos': soma_pontos if soma_pontos is not None else 0,
                'dias_sem_matricula': dias_sem_matricula,
                'cor': cor
            })

        context['contagem_matriculas'].sort(key=lambda x: x['contagem'], reverse=True)
        context['num_linhas'] = range(1, len(context['contagem_matriculas']) + 1)

    return render(request, 'matriculas/consulta.html', context)

