import json
import secrets
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from .models import Bread, SaleItem, Campaing, InstagramUser

class IndexView(TemplateView):
    template_name = 'index.html'
    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     product_list = Bread.objects.all()

    #     sale_item_list = list()
    #     for product in product_list:
    #         sale_item_list.append(SaleItem(item = product, quantity = 1, price_sum = product.price)) 
        
    #     campaing = Campaing.objects.filter(active=True).first()

    #     context['item_sale_list'] = sale_item_list
    #     context['campaing_date'] = campaing.delivery_date

        #return context


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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        entry = body["entry"][0]
        messaging = entry["messaging"][0]
        message = messaging["message"]
        
        if message["attachments"][0]["type"] == "story_mention":
            sender_id = messaging["sender"]["id"]
            timestamp = messaging["timestamp"]
            message_id = message["mid"]
            
            instagramUser = InstagramUser(
                user_name=sender_id,
                post_date=datetime.fromtimestamp(timestamp / 100),
                post_id=message_id,
                token=secrets.token_hex(3)[:6].upper(),
                json=timestamp
            )

            instagramUser.save()

            return HttpResponse(
                json.dumps(body),
                content_type="application/json"
            )
    
    if request.method == 'GET':
        mode         = request.GET.get("hub.mode")
        challenge    = request.GET.get("hub.challenge")
        verify_token = request.GET.get("hub.verify_token")

        if verify_token == 'abb0c1a0-509a-4694-b595-4c616b636661':
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

# def process_payment(request):

#     if request.method == 'POST':
#         payment_data = {
#             "transaction_amount": 100,
#             "description": "Título do produto",
#             "payment_method_id": "pix",
#             "payer": {
#                 "email": "demonteiro04@gmail.com",
#                 "first_name": "Débora",
#                 "last_name": "Pianco",
#                 "identification": {
#                     "type": "CPF",
#                     "number": "45068180831"
#                 },
#                 "address": {
#                     "zip_code": "06233-200",
#                     "street_name": "Av. das Nações Unidas",
#                     "street_number": "3003",
#                     "neighborhood": "Bonfim",
#                     "city": "Osasco",
#                     "federal_unit": "SP"
#                 }
#             }
#          }

#         payment_response = sdk.payment().create(payment_data)
#         payment = payment_response["response"]['point_of_interaction']['transaction_data']
#         return render(
#             request,
#             'payment.html',
#             {'payment': payment }
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )
   