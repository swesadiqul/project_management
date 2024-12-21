# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Project, Task, Comment
# from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer


# # Create your views here.
# class ProjectList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         projects = Project.objects.filter(owner=request.user)
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProjectDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         project = Project.objects.filter(id=id, owner=request.user).first()
#         if not project:
#             return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, id):
#         project = Project.objects.filter(id=id, owner=request.user).first()
#         if not project:
#             return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProjectSerializer(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         project = Project.objects.filter(id=id, owner=request.user).first()
#         if not project:
#             return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
#         project.delete()
#         return Response({"message": "Project deleted"}, status=status.HTTP_204_NO_CONTENT)


# class TaskList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, project_id):
#         tasks = Task.objects.filter(project_id=project_id)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request, project_id):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(project_id=project_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CommentList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, task_id):
#         comments = Comment.objects.filter(task_id=task_id)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)

#     def post(self, request, task_id):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(task_id=task_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task, Comment, ProjectMember
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer, ProjectMemberSerializer
from users.models import User

class ProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, id):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        project = Project.objects.get(id=id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        data = request.data
        data['project'] = project_id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        comments = Comment.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        data = request.data
        data['task'] = task_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        comment = Comment.objects.get(id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, id):
        comment = Comment.objects.get(id=id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = Comment.objects.get(id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


