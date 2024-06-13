from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ServerSerializer
from .models import Server
from rest_framework.response import Response

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    
    def list(self,request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        
        if category:
           self.queryset  = self.queryset.filter(category__name=category) #category__name is we are filtering the category's with the help of there name in the server model as it is the Foreign key 
           
             
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=request.user)
             
           
        if qty :
            self.queryset = self.queryset[:int(qty)]
            

            
        serializer = ServerSerializer(self.queryset,many=True) 
    
        return Response(serializer.data)
