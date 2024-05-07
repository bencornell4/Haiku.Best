import json
import requests

from django.shortcuts import render
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status
from rest_framework.parsers import JSONParser

from haikujudge.models import Haiku
from haikujudge.serializers import HaikuSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from llamaapi import LlamaAPI
from decouple import config

llama = LlamaAPI(config('LLAMA_API'))

# Create your views here.

@api_view(['HEAD'])
def haiku_head(request):
    return Response({'success': True}, status=201)

@api_view(['GET'])
def haiku_top(request):
    top_models = Haiku.objects.order_by('-score')[:3]
    serializer = HaikuSerializer(top_models, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def haiku_judge(request):
    # Check if the action has already been performed today
    last_action_date = request.session.get('last_haiku_judge_date', None)
    print(last_action_date)
    print(timezone.localdate())
    if last_action_date and last_action_date == timezone.localdate().isoformat():
        return Response({'message': 'one haiku a day'}, status=201)
    #extract haiku
    data = JSONParser().parse(request)
    haiku_serializer = HaikuSerializer(data=data)
    if haiku_serializer.is_valid():
        haiku_content = haiku_serializer.validated_data.get('content', '')
        author = haiku_serializer.validated_data.get('author', '')            
        #params
        accuracy = 1
        haiku_category = "Haiku"
        #prompt
        prompt_instructions = 'Rate the following Haiku on a scale of 0-10, please only respond with the number and nothing else.  Please use decimals to two decimal places.  A category will also be supplied that the Haiku should somewhat adhere to.  Do your best to be as consistent as possible so that if I were to give you this Haiku again, you would give it the same score.  Please rate critically because only a truly amazing Haiku should get a high score.  Lastly, here is a rubric: 0-3: does not follow the category or does not resemble a haiku.  3-5: a below average piece of poetry, about as good as poems found in a highschool poetry class. 5-7: passable poetry, about as good as poems found in a college poetry class.  7-9: a poem that could be published.  9-10: as good as any poem ever written, maybe better. Thank you in advance for your rating. The category of the Haiku is: ' + haiku_category
        #back to normal
        prompt_haiku = 'And the Haiku is: ' + haiku_content
        #initialize ollama post
        sum = 0
        llama_request_json = {
            'model': 'llama3-70b',
            'messages': [
                {'role': 'system', 'content': prompt_instructions},
                {'role': 'user', 'content': prompt_haiku},
            ],
            'stream': False
        }
        #run multiple times and average for consistency
        for i in range(accuracy):
            #post to ollama
            llama_response = llama.run(llama_request_json)
            result = llama_response.json()
            sum += float(result['choices'][0]['message']['content'])
        #create postgreSQL entry
        haiku = Haiku.objects.create(content=haiku_content, score=sum / accuracy, author=author)
        print('Successfully reviewed poem: ' + str(haiku.score))
        request.session['last_haiku_judge_date'] = timezone.localdate().isoformat()
        request.session.save()
        return Response({'score': haiku.score}, status=201)
    return Response({'error': 'Invalid JSON'}, status=400)
