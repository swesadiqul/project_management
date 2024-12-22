from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task, Comment, ProjectMember
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer, ProjectMemberSerializer
from users.models import User
from django.shortcuts import get_object_or_404


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Error fetching projects: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"message": "Project created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid input", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        serializer = ProjectSerializer(project)
        return Response({"message": "Project details retrieved", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        project = get_object_or_404(Project, id=id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Project updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid input", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        project = get_object_or_404(Project, id=id)
        project.delete()
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"success": True, "message": "Tasks retrieved.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        data = request.data.copy()
        data['project'] = project_id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response({"success": True, "message": "Task created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": "Task creation failed.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response({"success": True, "message": "Task retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Task updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Failed to update task.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return Response({"success": True, "message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response({"success": True, "message": "Comments retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        data = request.data.copy()
        data['task'] = task_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "message": "Comment created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": "Failed to create comment.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectMemberListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        members = ProjectMember.objects.filter(project=project)
        serializer = ProjectMemberSerializer(members, many=True)
        return Response({"success": True, "message": "Project members retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        user_id = request.data.get('user')
        role = request.data.get('role')

        if not user_id or not role:
            return Response({"success": False, "message": "User ID and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # Check if user is already a member of the project
        if ProjectMember.objects.filter(project=project, user=user).exists():
            return Response({"success": False, "message": "User is already a member of this project."}, status=status.HTTP_400_BAD_REQUEST)

        member = ProjectMember.objects.create(project=project, user=user, role=role)
        serializer = ProjectMemberSerializer(member)
        return Response({"success": True, "message": "Member added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class ProjectMemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, member_id):
        project = get_object_or_404(Project, id=project_id)
        member = get_object_or_404(ProjectMember, id=member_id, project=project)

        role = request.data.get('role')
        if not role:
            return Response({"success": False, "message": "Role is required."}, status=status.HTTP_400_BAD_REQUEST)

        member.role = role
        member.save()
        serializer = ProjectMemberSerializer(member)
        return Response({"success": True, "message": "Member role updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, project_id, member_id):
        project = get_object_or_404(Project, id=project_id)
        member = get_object_or_404(ProjectMember, id=member_id, project=project)
        member.delete()
        return Response({"success": True, "message": "Member removed successfully."}, status=status.HTTP_204_NO_CONTENT)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response({"success": True, "message": "Comment retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Comment updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Failed to update comment.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response({"success": True, "message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


