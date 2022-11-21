import os
import requests
from jiwer import cer
import base64
from pathlib import Path
from datetime import datetime

api_url = os.environ.get("API_URL", "127.0.0.1:5000")

output = '''
============================
    Predict test
============================

request done at "predict" at {current_date}
Make prediction on 5 img and test that the Character Error Rate (CER) is under an acceptable range

acceptable cer = {acceptable_cer} %
actual cer = {actual_cer} %

==>  {test_status}

'''

login_resp = requests.post(
    url='http://{url}/login'.format(url=api_url),
    json = { 'username': 'admin', 'password': 'admin' }
)

pymanotoken = login_resp.json()["token"]
acceptable_cer = 20

file_dir = os.path.dirname(__file__)
test_img_dir = os.path.join(file_dir,'test_img/')

actual_words = []
expected_words = []        
for filename in os.listdir(test_img_dir):
    f = os.path.join(test_img_dir, filename)
    with open(f, "rb") as image_file:                
        base64_img = base64.b64encode(image_file.read())   
        imageData = "data:image/png;base64," + base64_img.decode("utf-8") 
        
        r = requests.post(
            url='http://{url}/login'.format(url=api_url),
            headers={"x-access-token": pymanotoken},
            json= {"imageData" : imageData} 
        )
        actual_word = r.text                           
        actual_words.append(actual_word)
    expected_words.append(Path(f).stem)
actual_cer = cer(actual_words, expected_words) * 100  

# affichage des résultats
if actual_cer < acceptable_cer:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
formatted_output = output.format(current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"), acceptable_cer=acceptable_cer, actual_cer=round(actual_cer, 2), test_status=test_status)
print(formatted_output)

# impression dans un fichier
if str(os.environ.get('LOG')) == '1':        
    with open('./tests-results/api_test.log', 'a') as file:
        file.write(formatted_output)