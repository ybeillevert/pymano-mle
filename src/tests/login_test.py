import os
import requests
from datetime import datetime

api_url = os.environ.get("API_URL", "127.0.0.1:5000")

tests = [
    {
        'username' : 'bob',
        'password' : 'builder',
        'expected' : 201,
        'token_returned' : True
    },
    {
        'username' : 'bob',
        'password' : 'sponge',
        'expected' : 401,
        'token_returned' : False
    },
    {
        'username' : 'cake',
        'password' : 'sponge',
        'expected' : 401,
        'token_returned' : False
    }
]


output = '''
============================
    Login test
============================

request done at "login" at {current_date}
| username={username}
| password={password}

expected result = {expected}
actual restult = {status_code}

==>  {test_status}

'''

for test in tests:

    # requête
    r = requests.post(
        url='http://{url}/login'.format(url=api_url),
        json={"username": test['username'], "password": test['password']}
    )

    # statut de la requête
    status_code = r.status_code
    expected = test['expected']

    # affichage des résultats
    if status_code == expected and (not test['token_returned'] or  r.json()["token"]):
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    formatted_output = output.format(current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"), username=test['username'], password=test['password'], expected=expected, status_code=status_code, test_status=test_status)
    print(formatted_output)

    # impression dans un fichier
    if str(os.environ.get('LOG')) == '1':        
        with open('./tests-results/api_test.log', 'a') as file:
            file.write(formatted_output)