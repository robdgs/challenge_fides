from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from . serializer import *
from rest_framework.response import Response
# Create your views here.
class ReactView(APIView):
	def get(self, request):
		output = [{"lunghezzaPipo": output.lunghezzaPipo,
			  "larghezzaPipo": output.larghezzaPipo,
			    "altezzaPipo": output.altezzaPipo,
				  "persona": output.persona}
				  for output in React.objects.all()]
		return Response(output)

	def post(self, request):
		serializer = ReactSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)
	def put(self, request, pk):
		output = React.objects.get(id=pk)
		serializer = ReactSerializer(instance=output, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)
	def delete(self, request, pk):
		output = React.objects.get(id=pk)
		output.delete()
		return Response("Deleted")