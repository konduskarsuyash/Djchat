from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ServerSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import Server
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from .schema import server_list_docs    

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    permission_classes = [IsAuthenticated]
    
    @server_list_docs
    def list(self, request):
        """
        List servers based on provided query parameters.

        This method allows you to retrieve a list of servers with various filtering options,
        such as filtering by category, user membership, server quantity, and specific server ID.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.

        Returns:
            Response: A response containing serialized server data based on the provided filters.

        Raises:
            AuthenticationFailed: If the user is not authenticated.
            ValidationError: If validation errors occur during filtering, such as an invalid server ID.

        Example:
        To list servers with the following filters:
        - Filter by the category "gaming"
        - Limit results to 10 servers
        - Show only the servers where the user is a member
        - Filter for a server with ID 5

        `GET /servers/?categories=gaming&qty=10&by_user=true&by_server_id=5`

        Query Parameters:
        - `categories` (str): Filter servers by a specific category name.
        - `qty` (int): Limit the number of server results to a specific quantity.
        - `by_user` (bool): Filter servers based on user membership (true/false).
        - `by_server_id` (int): Filter servers by a specific server ID.
            Useful for retrieving detailed information about a single server.

        Filtering Logic:
        - Servers are filtered by category name if the 'categories' parameter is provided.
        - Servers are filtered by user membership if the 'by_user' parameter is set to "true".
        - The 'qty' parameter limits the number of server results returned.
        - The 'by_server_id' parameter retrieves details for a specific server by its ID.

        Response Format:
            The response contains serialized server data in a JSON format.

        Server Annotation:
            If the resulting queryset contains servers, the queryset is annotated with the
            number of members each server has, providing insight into server popularity.

        Note:
            Use proper authentication to access this endpoint, as indicated by the
            'AuthenticationFailed' exception that is raised when not authenticated.
        """

        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get('with_num_members') == 'true'


        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=request.user)
            else:
                raise AuthenticationFailed()
                

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))



        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail=f"Server value error")
        
        if qty:
            self.queryset = self.queryset[:int(qty)]

        serializer_context = {'num_members': with_num_members}
        serializer = ServerSerializer(self.queryset, many=True, context=serializer_context)

        return Response(serializer.data)