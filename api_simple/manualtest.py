import requests

URL = "http://127.0.0.1:5000/"

response_get_hello = requests.get(URL + "helloworld/")

print(response_get_hello.json())

response_get_square = requests.post(URL + "square", {"number" : 10})

print(response_get_square.json())

# response_post_hello = requests.post(BASE + "helloworld/")

# print(response_post_hello.json())

# response_get_user = requests.get(BASE + "hellouser/charles")

# print(response_get_user.json())




response_get_user = requests.get(URL + "hellouser_validator/13")

print(response_get_user.json())
print(response_get_user.status_code)


# Request with a token
headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}

print(requests.post(URL + "delete/", "data", headers=headers).json())