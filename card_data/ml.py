import urllib.request
import json

with open("mlkey.txt") as f1:
    api = f1.read().rstrip('\n')
    base_url = "https://api.clashroyale.com/v1"
    endpoint = "/cards"
    request = urllib.request.Request(
                    base_url+endpoint,
                    None,
                    {
                        "Authorization": "Bearer %s" %api
                    }
            )
    response = urllib.request.urlopen(request).read().decode("utf-8")
    print(response)

