from django.shortcuts import render, HttpResponse
from .models import Sites
import json
# Create your views here.
def parse(request):
    if request.method=="GET":
        return HttpResponse('Only available for POST requests.')
    if request.body:
        try:
            data = request.body.decode('utf-8')
            json_data = json.loads(data)
            url, data = json_data["url"], json_data["technologies"]
            search = Sites.objects.filter(url=url)
            if search:
                site = search[0]
                if data:
                    site.json = data
                    site.save()
                    print(f'[*] Successfully updated {url}')
                    return HttpResponse('Successful update.')
                else:
                    print(f"[!] Data for {url} is empty.")
                    return HttpResponse('Failed to update as the new data is empty.')
            Sites.objects.create(url=json_data["url"], json=json_data["technologies"])
            print(f'[*] Successully added {url} to the DB')
            return HttpResponse('Successful creation.')
        except Exception as e:
            print(f'[!] Error occured while trying to parse the data of {url}.')
            print(e)
            return HttpResponse('Error.')
    else:
        print("[!] The request's body is empty.")
        return HttpResponse("Empty request.")