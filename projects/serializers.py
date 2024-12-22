from rest_framework import serializers
from .models import Project, ProjectMember, Task, Comment


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()
    project = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']
        read_only_fields = ['project'] 
