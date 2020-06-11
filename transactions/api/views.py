from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Account

from .serializers import AccountSerializer


class stats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        accounts = Account.objects.filter(user=request.user)

        serializer = AccountSerializer(instance=accounts, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'accounts': serializer.data,
        })
