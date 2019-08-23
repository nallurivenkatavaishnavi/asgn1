from django.shortcuts import render

# Create your views here.
import requests
import time
import logging
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view

logging.basicConfig(filename="logfile.log", level=logging.INFO)
@csrf_exempt
@api_view(['GET', 'POST',]) 
def github(request):

    user = {}
    username=""
    user1=[]
    global total_time
    db_start = time.time()
    print("---------------------------------")
    logging.info('%s request method \n', request.method)
    print(request.method)
    print("-"*100)
    if request.method == 'POST':
        d = request.body
        nd = d.decode('utf-8')
        username = nd.split("\"")[3]
        print(username)
	    # b'{\n\t"org":"verloop"\n}'    
    print("===================================")
    
    if 'org' in request.GET:
        username = request.GET['org']
        print(username)

    url = 'https://api.github.com/orgs/%s/repos' % username
    response = requests.get(url)
    duration = response.elapsed.total_seconds()
    # print(response.elapsed.total_seconds())
    # print(response)
    user1 = response.json()
    # print(len(user1), type(user1))
    dump = list(user1)
    # print(" ********************88 hi  ********************************")
    # print(type(dump[1]))
    li = []
    for i in range(len(dump)):
        var1 = dump[i]["name"]
        var2 = dump[i]["stargazers_count"]
        li.append([var2, var1])
    li.sort(reverse = True)
    result = []
    j = 0
    for i in li:
        result.append({ "name": i[1],"stars":i[0]})
        j+=1
        if(j>2):
            break
    user[ "results" ] = result
    
    print(li)
    print("=============================================================")
    print(result)
    total_time = time.time() - db_start
    print(total_time)
    #return Response(user)
    if request.method == 'POST':
        logging.info('response :  \n')
        logging.info(user)
        return Response(user)
        
    else:
        user["response_time_from_git"] = duration
        user["total_time"] = total_time
        user['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
        logging.info('response :  \n')
        logging.info(user)
        return render(request, 'createAPI/github.html', {'user': user})

