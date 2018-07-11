from django.shortcuts import render
from django.http import JsonResponse
from .search_info import main
import json

def index(request):
    return render(request, 'index.html')


def search_log(request):
    qid = request.POST.get('qid')
    result_list = main(qid)
    query = ''
    type = ''
    response = ''
    for result in result_list:
        query = result['query'] if result.get('query') else query
        type = result['type'] if result.get('type') else type
        response = result['response'] if result.get('response') else response

    context = {
        'type': type,
        'query': query,
        'result': response
    }
    return JsonResponse(context)


