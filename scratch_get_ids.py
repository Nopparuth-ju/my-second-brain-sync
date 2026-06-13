import urllib.request, re

handles = ['@TheStandardNews', '@KNDStudioOfficial']
headers = {'User-Agent': 'Mozilla/5.0'}

for h in handles:
    try:
        req = urllib.request.Request('https://www.youtube.com/' + h, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        m = re.search(r'\"externalId\":\"(UC[a-zA-Z0-9_-]+)\"', html)
        if m: 
            print(h, m.group(1))
        else: 
            print(h, 'Not found')
    except Exception as e:
        print(h, e)
