from django.shortcuts import render

@api_view(['POST'])
def create_client(request):

    name = request.data.get("name")
    cnpj = request.data.get("cnpj")


    if not name:
        return Response({'message': "invalid str"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    if not cnpj:
        return Response({'message': "invalid str"}, status=status.HTTP_400_BAD_REQUEST)
    
    if Client.objects.filter(name=name, cnpj=cnpj).exists():
        return Response({"message":"exists"}, status=status.HTTP_400_BAD_REQUEST)