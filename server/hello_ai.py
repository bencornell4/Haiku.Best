import json
import requests

#params
accuracy = 5
haikuCategory = "Haiku"

#haiku input
haiku = input("Enter your Haiku: ")

#prompt
prompt = 'Rate the following Haiku on a scale of 0-10, please only respond with the number and nothing else.  You may use decimals, for example 1.2 or 0.0.  A category will also be supplied that the Haiku should somewhat adhere to.  The Haiku must have syllable counts in the 5-7-5 pattern.  Do your best to be as consistent as possible so that if I were to give you this Haiku again, you would give it the same score.  Please rate critically because only a truly amazing Haiku should get a high score.  Lastly, here is a rubric: 0-3: does not follow the category or does not have the correct syllable count.  3-5: a below average piece of poetry, about as good as poems found in a highschool poetry class. 5-7: passable poetry, about as good as poems found in a college poetry class.  7-9: a poem that could be published.  9-10: as good as any poem ever written, maybe better. Thank you in advance for your rating. The category of the Haiku is: ' + haikuCategory + ' And the Haiku is: '
prompt += haiku
postData = {
    'prompt': prompt,
    'model': 'llama3',
    'stream': False
}
sum = 0
ollamaUrl = 'http://localhost:11434/api/generate'
for i in range(accuracy):
    llmResponse = requests.post(ollamaUrl, data=json.dumps(postData))
    result = llmResponse.json()
    sum += float(result['response'])
print('Your score is:', sum / accuracy)
