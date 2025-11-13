from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
import requests
import os
from google import genai
from dotenv import load_dotenv

import base64
import os
#from google import genai
from google.genai import types

class Views:

    def verify_authentication(self, request, callback):
        access_token : str = request.headers['Authorization'] 
        access_token = access_token.split(' ')[1]
        
        print(access_token)
        body = {"token" : access_token}
        print(body)
        validacao = requests.post(url=f'{os.getenv('AUTH_URL')}api/token/verify/', data=body)
        validacao = validacao.json()
        print(f"validando:{validacao}")

        if validacao != {}:
            return Response(validacao, status=status.HTTP_401_UNAUTHORIZED)
        
        return callback(request)

class CreateTaskView(generics.CreateAPIView,Views):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def post(self, request, *args, **kwargs):
        self.verify_authentication(request,self.create)

    

class GetTaskView(generics.ListAPIView,Views):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        self.verify_authentication(request,self.list)

    

class PatchTaskView(generics.UpdateAPIView,Views):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        return Response({"mensagem": "Operação não permitida"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        return self.verify_authentication(request,self.partial_update)

class DeleteTaskView(generics.DestroyAPIView,Views):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.verify_authentication(request,self.destroy)



class ChooseUserToDoTask(APIView,Views):

    def verify_authentication(self, request, callback,pk):
        access_token : str = request.headers['Authorization'] 
        access_token = access_token.split(' ')[1]
        
        print(access_token)
        body = {"token" : access_token}
        print(body)
        validacao = requests.post(url=f'{os.getenv('AUTH_URL')}api/token/verify/', data=body)
        validacao = validacao.json()
        print(f"validando:{validacao}")

        if validacao != {}:
            return Response(validacao, status=status.HTTP_401_UNAUTHORIZED)
        
        return callback(request,pk)

    def get(self, request,pk, *args, **kwargs):
        return self.verify_authentication(request,self.chooseUser,pk)

    
    def chooseUser(self, request,pk, *args, **kwargs):
        load_dotenv()
        mode = request.query_params.get('mode')

        response = requests.get(f"{os.getenv("SKILL_URL")}/api/skill/users/")
        if response.status_code == 204:
            return Response({"mensagem": "Sem Usuários com habilidades cadastradas na base"},status=status.HTTP_204_NO_CONTENT)
        if response.status_code != 200:
            return Response({"mensagem":"Erro ao tentar pegar as habilidades dos usuários"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        users = []
        response = response.json()
        match mode:
            case 'proficiency':
                
                for user in response.keys():
                    users.append(
                        {
                            user: [{skill["habilidade"]: skill["proeficiencia"]} for skill in response[user]]
                        }
                    )
            case 'knowledge':
                for user in response.keys():
                    users.append(
                        {
                            user: [{skill["habilidade"]: skill["proeficiencia"]} for skill in response[user] if skill["aprendendo"]]
                        }
                    )
            case _:
                return Response({"mensagem": "Modo inválido"}, status=status.HTTP_400_BAD_REQUEST)
        print(pk)
        task = Task.objects.get(id=pk)
        print(task.descricao)
        input = {
            "mode": mode,
            "taskTitle": pk,            
            "taskDescription": task.descricao,
            "users": users
        }
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-2.5-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"{str(input)}"),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=-1,
            ),
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["topChoice", "hoursToCompleteTask", "reasonWhyTopChoiceIsBetter"],
                properties = {
                    "topChoice": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                    "hoursToCompleteTask": genai.types.Schema(
                        type = genai.types.Type.NUMBER,
                    ),
                    "reasonWhyTopChoiceIsBetter": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                },
            ),
            system_instruction=[
                types.Part.from_text(text="""You are a agile manager, you need to evaluate a task by the needed knoledge to complete, and find in a list of users the best match to complete the task. There are two modes to find, by proficiency and knowledge. If the mode is proficiency, you will recive a description of the task and a list of users ID and their respective abilities. If the mode is knowledge you shall instead of what they know it will be a list of skills that they want to learn."""),
            ],
        )
        mensagem = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        return Response(mensagem.parsed)
        
        