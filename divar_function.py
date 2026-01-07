import requests,uuid,os
from dotenv import load_dotenv
def get_number(token,authorization):
    contact_uuid = str(uuid.uuid4())
    url=f'https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}'
    data={"contact_uuid":contact_uuid}
    headers={'authorization':authorization,
         "content-type":"application/json"}
    res=requests.post(url,json=data,headers=headers)

    for i in range(3):
        try:
            phone_number=res.json()['widget_list'][i]['data']['action']['payload']['phone_number']
            break
        except:
            pass
    else:
        print(res.json())
        phone_number=''
            
    return phone_number
load_dotenv()
authorization=os.getenv("authorization")
token='gZn4ITPT'
phon=get_number(token=token,authorization=authorization)
print(phon)