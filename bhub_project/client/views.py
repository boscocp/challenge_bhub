from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from client.serializers import ClienteSerializer, DadosBancariosSerializer
from client.models import Cliente, DadosBancarios
from django.core.exceptions import ValidationError


# Create your views here.
class ClienteView(APIView):
    def post(self, request):
        try:
            cliente_serializer = ClienteSerializer(
                data=request.data['cliente'])
            # TODO: criar validacao customisada
            cliente_serializer.is_valid(raise_exception=True)
            cliente_serializer.save()
            response = Response()
            response.data = {
                'cliente': 'Cliente criado com sucesso'
            }
            response.status_code = 201
            return response
        except ValidationError as error:
            return Response({'message': error.message}, status=400)
        except Exception:
            return Response({'message': 'Erro ao cadastrar cliente'}, status=400)

    def get(self, request, **pk):
        if pk:
            cliente = get_object_or_404(Cliente, uuid=pk['pk'])
            serialized = ClienteSerializer(cliente)
            return Response(serialized.data)
        else:
            clientes = Cliente.objects.all()
            serializer = ClienteSerializer(clientes, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        cliente = get_object_or_404(Cliente, uuid=pk)
        try:
            serializer = ClienteSerializer(
                cliente, data=request.data['cliente'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as error:
            return Response({'message': error.message}, status=400)
        except Exception:
            return Response({'message': 'Erro ao cadastrar cliente'}, status=400)

    def delete(self, request, pk):
        get_object_or_404(Cliente, uuid=pk).delete()
        response = Response()
        response.data = {
            'cliente': 'Cliente deletado com sucesso',
        }
        response.status_code = 204
        return response


class DadosBancariosView(APIView):
    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, uuid=pk)
        try:
            dadosbancarios_serializer = DadosBancariosSerializer(
                data=request.data['dadosbancarios'])
            dadosbancarios_serializer.is_valid(raise_exception=True)
            dadosbancarios = dadosbancarios_serializer.save()
            cliente.dadosbancarios_set.add(dadosbancarios, bulk=False)
            response = Response()
            response.data = {
                'cliente': 'Dados bancarios criado com sucesso',
            }
            response.status_code = 201
            return response
        except ValidationError as error:
            return Response({'message': error.message}, status=400)
        except Exception:
            return Response({'message': 'Erro ao cadastrar dados bancarios'}, status=400)

    def get(self, request, **pk):
        cliente = get_object_or_404(Cliente, uuid=pk['pk'])
        if 'db_id' not in pk.keys():
            dadosbancarios = DadosBancarios.objects.filter(
                cliente__uuid=pk['pk'])
            serializer = DadosBancariosSerializer(dadosbancarios, many=True)
            return Response(serializer.data)
        else:
            dadosbancarios = DadosBancarios.objects.get(uuid=pk['db_id'])
            serializer = DadosBancariosSerializer(dadosbancarios)
            return Response(serializer.data)

    def put(self, request, **pk):
        try:
            dadosbancarios = get_object_or_404(
                DadosBancarios, uuid=pk['db_id'])
            serializer = DadosBancariosSerializer(
                dadosbancarios, data=request.data['dadosbancarios'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as error:
            return Response({'message': error.message}, status=400)
        except Exception:
            return Response({'message': 'Erro ao cadastrar dados bancarios'}, status=400)

    def delete(self, request, **pk):
        get_object_or_404(DadosBancarios, uuid=pk['db_id']).delete()
        response = Response()
        response.data = {
            'dadosbancarios': 'Dados Bancarios deletados com sucesso',
        }
        response.status_code = 204
        return response
