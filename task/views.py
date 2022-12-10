from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.

# Home do Projeto

def home(request):
    return render(request,'home.html')


def sigup(request):

    if request.method == 'GET':

        return render(request,'sigup.html', {
            'form' : UserCreationForm
        } )   

    else: 
        if request.POST['password1'] == request.POST['password2']:

            try: 
                
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                
                login(request, user)
               
                return redirect('tasks')
                
            except:
                return render (request,'sigup.html', { 
                    'form' : UserCreationForm ,
                    "error": 'Usuário já existe'
                    
                    } ) 
           
        return render (request,'sigup.html', { 
                    'form' : UserCreationForm ,
                    "error": 'senhas são diferentes'
                    
                    } ) 

def sigin(request):

    if request.method == 'GET':
        return render(request,'sigin.html', {
        'form': AuthenticationForm
        })

    else:
        user = authenticate(

            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'sigin.html', {
                    'form' : AuthenticationForm,
                    'error': 'Usuário ou senha está incorreto'
                })

        else:
                login(request, user)
                return redirect('tasks')    


@login_required   
def sair(request):
    logout (request)
    return redirect('home')

@login_required       
def tasks(request):
    return render(request,'tasks.html')

@login_required  
def criando_tarefa(request):

    if request.method == 'GET':
        return render(request, 'criando_tarefa.html', {
            'form' : TaskForm
        })

    else:

        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError:

            return render(request,'criando_tarefa.html', {
                'form' : TaskForm,
                'error' : 'Favor inserir dados validos'
            })      


@login_required  
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) 
    return render(request, 'tasks.html', { 'tasks' : tasks })



@login_required  
def task_detalhe(request, task_id): 

    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  # tenho que importar o get_object_or_404 serve para so ids das tarefas
        form = TaskForm(instance=task)
        return render(request,'task_detalhe.html', {'task': task, 'form': form}) 

    else:  
        try: 
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')

        except ValueError:
            return render(request,'task_detalhe.html', {'task': task, 'form': form,
            'error': "Erro ao atualizar a tarefa"}) 

#completar tarefa
@login_required  
def complete_tarefa(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

#deletar tarefa
@login_required  
def deletar_tarefa(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


#exibir todas as tarefas completadas
@login_required  
def exibir_tarefas_completadas(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by 
    ('-datecompleted') 
    return render(request, 'tasks.html', { 'tasks' : tasks })