import json
import requests
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from haikujudge.models import Haiku
from haikujudge.serializers import HaikuSerializer
from rest_framework.decorators import api_view

from llamaapi import LlamaAPI
from decouple import config

llama = LlamaAPI(config('LLAMA_API'))

# Create your views here.

@api_view(['POST'])
def haiku_judge(request):
    #extract haiku
    data = JSONParser().parse(request)
    haiku_serializer = HaikuSerializer(data=data)
    if haiku_serializer.is_valid():
        #find out waht this does
        haiku_serializer.save()
        #this isnt right
        haiku_content = haiku_serializer.validated_data.get('content', '')
        author = haiku_serializer.validated_data.get('author', '')            
        #params
        accuracy = 1
        haiku_category = "Haiku"
        #prompt
        prompt_instructions = 'Rate the following Haiku on a scale of 0-10, please only respond with the number and nothing else.  You may use decimals, for example 1.2 or 0.0.  A category will also be supplied that the Haiku should somewhat adhere to.  The Haiku must have syllable counts in the 5-7-5 pattern.  Do your best to be as consistent as possible so that if I were to give you this Haiku again, you would give it the same score.  Please rate critically because only a truly amazing Haiku should get a high score.  Lastly, here is a rubric: 0-3: does not follow the category or does not have the correct syllable count.  3-5: a below average piece of poetry, about as good as poems found in a highschool poetry class. 5-7: passable poetry, about as good as poems found in a college poetry class.  7-9: a poem that could be published.  9-10: as good as any poem ever written, maybe better. Thank you in advance for your rating. The category of the Haiku is: ' + haiku_category
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
        return JsonResponse({'score': haiku.score}, status=201)
    return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
