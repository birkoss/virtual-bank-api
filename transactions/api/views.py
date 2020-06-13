from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Account, TransactionCategory

from .serializers import AccountSerializer


class transactionsCategories(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = TransactionCategory.objects.filter(
            user=request.user).order_by("name")
        serializer = TaskSerializer(instance=categories, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'tasks': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TransactionCategoryWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


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
