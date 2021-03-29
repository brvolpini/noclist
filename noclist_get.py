import requests
import hashlib
import sys
import json

url_auth = "http://API-ENDPOINT-IP:8888/auth"
url_users = "http://API-ENDPOINT-IP:8888/users"

#Handling errors
attempts = 0
while attempts < 3:
  try:
    req = requests.head(url_auth).headers

    token =  req.get('Badsec-Authentication-Token')



    # Generating Hash
    def generate_hash(secret, param_str):
        dk = hashlib.sha256()
        s = secret + param_str
        dk.update(s.encode('utf-8'))
        return dk.hexdigest().upper()

    # Checksum Calculation with token and path
    checksum_calc = generate_hash(token, "/users")


    headers = {'X-Request-Checksum': checksum_calc}

    #Request the ids
    request_users_ids = requests.request("GET", url_users, headers=headers).text.encode('utf-8').decode('utf8')
    
    # format output to get a python list 
    id_list  = request_users_ids.splitlines()

    print(id_list)
    break

  except Exception as e:
      attempts+=1
      if attempts < 3:
          print("retrying")
      else:
          print("ERROR: ", e)

