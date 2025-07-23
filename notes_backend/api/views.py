from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from .models import Note
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class NoteViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing notes.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the notes
        for the currently authenticated user.
        """
        return self.request.user.notes.all().order_by('-updated_at')

    def perform_create(self, serializer):
        """
        Associate the note with the logged-in user.
        """
        serializer.save(user=self.request.user)
