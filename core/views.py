import json
import websocket
import secrets
import time
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from .models import InstagramUser

class IndexView(TemplateView):
    template_name = 'index.html'

@csrf_exempt
def verify_token(request):
    if request.method == 'POST':
        # Obtenha o token do corpo da solicitação
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        token = body['token']

        try:
            instagramUser = InstagramUser.objects.get(token=token)
            if not instagramUser.rewarded:
                ws = websocket.WebSocket()
                ws.connect("ws://192.168.0.16:80/ws")  # Substitua pelo endereço IP do seu servidor Wemos D1
                ws.send("ligar")
                
                time.sleep(10)  # Aguardar 3 segundos
                
                ws.send("desligar")
                ws.close()  # Fechar a conexão imediatamente após o envio da mensagem

                instagramUser.rewarded = Trueverc
                instagramUser.rewarded_date = datetime.now()
                instagramUser.save()

                return JsonResponse({'message': f'Parabéns {instagramUser.post_id}, Recebe sua recompensa!', 'status': 'success'})
            else:
                return JsonResponse({'message': f'Usuário {instagramUser.post_id} já recompensado.', 'status': 'error'})
        except InstagramUser.DoesNotExist:
            return JsonResponse({'message': 'Código inválido.', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Método não permitido.', 'status': 'error'})



@csrf_exempt
def mentioned(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        
        auth_token = data['auth_token']
        if auth_token == os.environ.get("TOKEN"):
            username = data['username']
            full_name = data['full_name']

            secret_token = secrets.token_hex(3)[:6].upper()

            instagramUser = InstagramUser(
                user_name=username,
                post_date=datetime.now(),
                post_id=full_name,
                token=secret_token,
                json=json.dumps(request.body.decode('utf-8'))
            )

            instagramUser.save()

            return HttpResponse(
                json.dumps({'token': secret_token}),
                content_type="application/json"
            )
        else:
             return HttpResponse(
                json.dumps({'message': 'Não autorizado.'}),
                content_type="application/json"
            )
    
    if request.method == 'GET':
        mode         = request.GET.get("hub.mode")
        challenge    = request.GET.get("hub.challenge")
        verify_token = request.GET.get("hub.verify_token")

        if verify_token == os.environ.get("TOKEN"):
            return HttpResponse(
                challenge ,
                content_type="application/json"
            )
        
        return HttpResponse('Token Fail')


def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
