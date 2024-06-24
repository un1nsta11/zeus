import requests


# http://biogance.com/wp-content/uploads/smush-600a5815c9a7a5ef3f9e.log

response = requests.get("http://biogance.com/wp-content")
print(response.text)
