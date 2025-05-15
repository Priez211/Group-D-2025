from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
def get_unread_count(request):
    if not request.user.is_authenticated:
        return Response({'count': 0})
    
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return Response({'count': count}) 