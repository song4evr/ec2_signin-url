import urllib, json, sys
import requests # 'pip install requests'
import boto3 # AWS SDK for Python (Boto3) 'pip install boto3'


# this code changed a little bit from the python example code of
# "Enabling custom identity broker access to the AWS console"

# learn more from the URL below. 
# https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html#STSConsoleLink_programPython

def get_login_url():

    session = boto3.Session()
    credentials = session.get_credentials()
    
    
    url_credentials = {}
    url_credentials['sessionId'] = credentials.access_key
    url_credentials['sessionKey'] = credentials.secret_key
    url_credentials['sessionToken'] = credentials.token
    json_string_with_temp_credentials = json.dumps(url_credentials)
    
    
    request_parameters = "?Action=getSigninToken"
    request_parameters += "&SessionDuration=43200"
    if sys.version_info[0] < 3:
        def quote_plus_function(s):
            return urllib.quote_plus(s)
    else:
        def quote_plus_function(s):
            return urllib.parse.quote_plus(s)
    request_parameters += "&Session=" + quote_plus_function(json_string_with_temp_credentials)
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    r = requests.get(request_url)
    
    signin_token = json.loads(r.text)
    
    
    request_parameters = "?Action=login" 
    request_parameters += "&Issuer=Example.org" 
    request_parameters += "&Destination=" + quote_plus_function("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token["SigninToken"]
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    
    return(request_url)
    
    
if __name__ == "__main__":
    print(get_login_url())