import json
import requests
import secrets
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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        token = body['token'] 
        
        try:
            instagramUser = InstagramUser.objects.get(token=token)
            if not instagramUser.rewarded:
                instagramUser.rewarded = True
                instagramUser.rewarded_date = datetime.now()
                instagramUser.save()

                
                return JsonResponse({'message': f'Parabéns {instagramUser.user_name}, Recebe sua recompensa!', 'status': 'success'})
            else:
                return JsonResponse({'message': f'Usuário {instagramUser.user_name} já recompensado.', 'status': 'error'})
        except InstagramUser.DoesNotExist:
            return JsonResponse({'message': 'Código inválido.', 'status': 'error'})
    
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
