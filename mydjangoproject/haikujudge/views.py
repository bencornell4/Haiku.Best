import json
import requests

from django.shortcuts import render
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Window, F
from django.db.models.functions import PercentRank

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

@api_view(['GET'])
def haiku_head(request):
    last_action_date = request.session.get('last_haiku_judge_date', None)
    last_action_score = request.session.get('last_haiku_judge_score', None)
    last_action_percentile = request.session.get('last_haiku_judge_percentile', None)
    if last_action_date and last_action_date == timezone.localdate().isoformat():
        return Response({'alreadySubmitted': True, 'lastScore': last_action_score, 'lastPercentile': last_action_percentile}, status=201)
    return Response({'alreadySubmitted': False}, status=201)

@api_view(['GET'])
def haiku_top(request):
    top_models = Haiku.objects.order_by('-score')[:3]
    serializer = HaikuSerializer(top_models, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def haiku_judge(request):
    # Check if the action has already been performed today
    last_action_date = request.session.get('last_haiku_judge_date', None)
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
        prompt_instructions = 'Rate the following Haiku on a scale of 0-10 using decimals, please only respond with the number and nothing else.  A category will also be supplied that the Haiku should somewhat adhere to.  Please rate critically because only a truly amazing Haiku should get a high score.  Lastly, here is a rubric: 0-3: does not follow the category or does not resemble a haiku.  3-5: a below average piece of poetry, about as good as poems found in a highschool poetry class. 5-7: passable poetry, about as good as poems found in a college poetry class.  7-9: a poem that could be published.  9-10: as good as any poem ever written, maybe better. Thank you in advance for your rating. The category of the Haiku is: ' + haiku_category
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
        
        #generate score percentile
        haikus_by_percentile = Haiku.objects.annotate(
            percentile_rank=Window(
                expression=PercentRank(),
                order_by=F('score').desc()
            )
        )

        # Find the percentile rank of the current haiku within the context of all haikus
        for item in haikus_by_percentile:
            if item.id == haiku.id:
                percentile_score = round(item.percentile_rank * 100, 2)
                break

        # Convert percentile rank to percentage for display
        #store session data
        print('Successfully reviewed poem: ' + str(haiku.score))
        request.session['last_haiku_judge_date'] = timezone.localdate().isoformat()
        request.session['last_haiku_judge_score'] = str(haiku.score)
        request.session['last_haiku_judge_percentile'] = str(percentile_score)
        request.session.save()
        return Response({'score': haiku.score, 'percentile_score': percentile_score}, status=201)
    return Response({'error': 'Invalid JSON'}, status=400)
