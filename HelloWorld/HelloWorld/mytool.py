def aaa_login(username, password, ip_addr):
    payload = {
        'aaaUser' : {
            'attributes' : {
                'name' : username,
                'pwd' : password
                }
            }
        }
    url = "https://" + ip_addr + "/api/aaaLogin.json"
    auth_cookie = {}

    response = requests.request("POST", url, data=json.dumps(payload), verify=False)
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)['imdata'][0]
        token = str(data['aaaLogin']['attributes']['token'])
        auth_cookie = {"APIC-cookie" : token}

    print
    print "aaaLogin RESPONSE:"
    print json.dumps(json.loads(response.text), indent=2)

    return response.status_code, auth_cookie

def aaa_logout(username, ip_addr, auth_cookie):
    payload = {
        'aaaUser' : {
            'attributes' : {
                'name' : username
                }
            }
        }
    url = "https://" + ip_addr + "/api/aaaLogout.json"

    response = requests.request("POST", url, data=json.dumps(payload),
                                cookies=auth_cookie, verify=False)

    print
    print "aaaLogout RESPONSE:"
    print json.dumps(json.loads(response.text), indent=2)
    print


def get(ip_addr, auth_cookie, url, payload):
    response = requests.request("GET", url, data=json.dumps(payload),
                                cookies=auth_cookie, verify=False)

    print
    print "GET RESPONSE:"
    print json.dumps(json.loads(response.text), indent=2)
    return response

def post(ip_addr, auth_cookie, url, payload):
    response = requests.request("POST", url, data=json.dumps(payload),
                                cookies=auth_cookie, verify=False)

    print ()
    print ("POST RESPONSE:")
    print (json.dumps(json.loads(response.text), indent=2))

