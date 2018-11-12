import requests as r

s1 = r.Session()
s2 = r.Session()

url = "http://127.0.0.1:5000/"
headers = {'Content-type': 'application/json'}

# d = {'user':'yash', 'pass':'deep'}
# resp = s1.post(url + 'login', json=d, headers=headers)
# print resp.text #, resp.headers
#
# d = {'user':'saini', 'pass':'yash'}
# resp = s2.post(url + 'login', json=d, headers=headers)
# print resp.text #, resp.headers
#
# d = {'user':'yash', 'pass':'deep'}
# resp = s1.post(url + 'logout', json=d, headers=headers)
# print resp.text #, resp.headers
#
# d = {'user':'saini', 'pass':'yash'}
# resp = s2.post(url + 'profile', json=d, headers=headers)
# print resp.text #, resp.headers

d = {
'user-mail' : 'abc@xyz.com',
'user-mob' : '99999999',
'user-name' : 'yash',
'user-pass' : 'asdasdasdpass'
}
resp = s2.post(url + 'register', json=d, headers=headers)
print resp.text #, resp.headers
