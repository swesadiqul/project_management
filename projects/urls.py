from django.urls import path
from .views import ProjectListView, ProjectDetailView, TaskListView, TaskDetailView, CommentListView, CommentDetailView


urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='projects-list'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/tasks/', TaskListView.as_view(), name='tasks-list'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/comments/', CommentListView.as_view(), name='comments-list'),
    path('comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
]
