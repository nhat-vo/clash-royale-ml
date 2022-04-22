import urllib.request
import json

with open("api_key_thon.txt") as f1:
    api = f1.read().rstrip('\n')
    url = "https://api.clashroyale.com/v1"
    endobject = "/cards"
    request = urllib.request.Request(
                    url+endobject,
                    None,
                    {
                        "Authorization": "Bearer %s" %api
                    }
            )
    response = urllib.request.urlopen(request).read().decode("utf-8")
    print(response)