from .views import CreateTaskView, GetTaskView, PatchTaskView, DeleteTaskView, ChooseUserToDoTask
from django.urls import path

urlpatterns = [
    path('task/create/', CreateTaskView.as_view(), name='task-create'),
    path('task/', GetTaskView.as_view(), name='task-get-all'),
    path('task/patch/<int:pk>/', PatchTaskView.as_view(), name='task-patch'),
    path('task/deletar/<int:pk>/', DeleteTaskView.as_view(), name='task-delete'),
    path('task/selectUser/<int:pk>/', ChooseUserToDoTask.as_view(), name='task-chooseUser')
]
