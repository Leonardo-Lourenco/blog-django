"""appYoutube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.home, name='home'),
    path('sigup/', views.sigup, name='sigup'),
    path('sigin/', views.sigin, name='sigin'),
    path('sair/', views.sair, name='sair'),
    path('tasks/', views.tasks, name='tasks'),
     path('criando/tarefa/', views.criando_tarefa, name='criando_tarefa'),
    path('criando/<int:task_id>/', views.task_detalhe, name='task_detalhe'), 
    path('criando/<int:task_id>/complete', views.complete_tarefa, name='complete_tarefa'), 
    path('criando/<int:task_id>/delete', views.deletar_tarefa, name='deletar_tarefa'), 
    path('exibir_tarefas_completadas', views.exibir_tarefas_completadas, name='exibir_tarefas_completadas'), 
    path('', include('blog.urls')),
]
