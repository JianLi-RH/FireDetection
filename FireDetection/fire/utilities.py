import requests

def post(url, data={}, headers={}):
    try:
        if not headers:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent' : user_agent, 'Content-type' : 'application/json'}

        r = requests.post(url=url, data=data, headers=headers)

        print(r.text)
    except Exception as ex:
        return r.text