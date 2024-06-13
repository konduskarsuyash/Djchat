from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ServerSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import Server
from rest_framework.response import Response
from django.db.models import Count

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

def list(self, request):
    """
    Retrieve a list of servers based on various query parameters.

    This view method handles the retrieval of a list of servers from the database based on the provided query parameters.
    The query parameters can be used to filter the servers by category, user, server ID, and specify the number of
    servers to return. Additionally, the method can annotate the queryset with the number of members for each server.

    Args:
        request (HTTPRequest): The incoming HTTP request object.

    Raises:
        AuthenticationFailed: If the user is not authenticated and a user-specific or server-specific filter is requested.
        ValidationError: If the provided server ID is invalid or does not exist.

    Returns:
        Response: A Django REST Framework Response object containing the serialized list of servers.

    Query Parameters:
        category (str, optional): Filter servers by the specified category name.
        qty (int, optional): Limit the number of servers returned.
        by_user (bool, optional): Filter servers by the authenticated user. True to include only servers the user is a member of.
        by_serverid (int, optional): Filter servers by the specified server ID.
        with_num_members (bool, optional): Include the number of members for each server in the response.
    """
    category = request.query_params.get('category')
    qty = request.query_params.get('qty')
    by_user = request.query_params.get('by_user') == 'true'
    by_serverid = request.query_params.get('by_serverid')
    with_num_members = request.query_params.get('with_num_members') == 'true'

    if by_user or by_serverid and not request.user.is_authenticated:
        raise AuthenticationFailed()

    if category:
        self.queryset = self.queryset.filter(category__name=category)

    if by_user:
        user_id = request.user.id
        self.queryset = self.queryset.filter(member=request.user)

    if with_num_members:
        self.queryset = self.queryset.annotate(num_members=Count('member'))

    if qty:
        self.queryset = self.queryset[:int(qty)]

    if by_serverid:
        try:
            self.queryset = self.queryset.filter(id=by_serverid)
            if not self.queryset.exists():
                raise ValidationError(detail=f"Server with id {by_serverid} not found")
        except ValueError:
            raise ValidationError(detail=f"Server value error")

    serializer_context = {'num_members': with_num_members}
    serializer = ServerSerializer(self.queryset, many=True, context=serializer_context)

    return Response(serializer.data)