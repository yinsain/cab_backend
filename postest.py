import requests as r

s1 = r.Session()
s2 = r.Session()

url = "http://127.0.0.1:5000/"
headers = {'Content-type': 'application/json'}

# d = {'user-mail':'vischugh@gmail.com', 'user-pass':'vishal'}
# resp = s1.post(url + 'login', json=d, headers=headers)
# print resp.text
# print 'HEADERS ---------------\n\n\n', resp.headers
#
#
# print '\n\n\n\nPROFILE FETCH TESTSTSTSTST'
# resp = s1.get(url + 'profile', headers=headers)
# print resp.text
# print 'HEADERS ---------------\n\n\n', resp.headers


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
#
# d = {
# 'user-mail' : 'yashdeep.saini@students.iiit.ac.in',
# 'user-mob' : '99999899',
# 'user-name' : 'yash',
# 'user-pass' : 'asdasdasdpass'
# }
#
# resp = s2.post(url + 'register', json=d, headers=headers)
# print resp.text, resp.headers
#
# d = {
# 'user-mail' : 'yashdeep.saini@students.iiit.ac.in',
# 'otp' : 'PN-6975919'
# }
# resp = s2.post(url + 'verify', json=d, headers=headers)
# print resp.text, resp.headers

#
# d = {
# 'source' : 'x',
# 'dest' : 'y',
# 'date' : '10/11/2018',
# 'seats' : '4',
# 'price' : '34.34',
# 'hour' : '10'
# }
#
# resp = s2.post(url + 'offer', json=d, headers=headers)
# print resp.text, resp.headers
#
# d = {
# 'source' : 'x',
# 'dest' : 'y',
# 'date' : '10/11/2018',
# 'seats' : '4',
# 'price' : '34.34',
# 'hour' : '10'
# }
#
# resp = s2.post(url + 'offered', json=d, headers=headers)
# print resp.text, resp.headers
#
# d = {
# 'source' : 'x',
# 'dest' : 'y',
# 'date' : '10/11/2018',
# 'seats' : '4',
# 'hour' : '10'
# }
#
# resp = s2.post(url + 'find', json=d, headers=headers)
# print resp.text, resp.headers

d = {
'rider-id' : '2'
}

resp = s2.post(url + 'subscribe', json=d, headers=headers)
print resp.text, resp.headers
