import requests,uuid
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

def singin_user(phon_number):
    url='https://api.divar.ir/v5/auth/authenticate'
    data={"phone":phon_number}
    headers={"content-type":"application/json"}
    res=requests.post(url,json=data,headers=headers)
    url='https://api.divar.ir/v5/auth/confirm'
    code=input("pleas enter activation code:  ")
    data={"phone":phon_number ,"code":code}
    res=requests.post(url,json=data,headers=headers)
    authorization=f"Basic {res.json()['token']}"
    return authorization

def serch_query(quary,city):
    url='https://api.divar.ir/v8/prediction/w/query'
    data={"query":quary,"cities":city}
    headers={"content-type":"application/json"}
    serche0=requests.post(url,json=data,headers=headers)
    if serche0.status_code != 200:
        return []
    table = []
    for s in serche0.json()["suggestions"]:
        table.append((
            s["title"],
            s["subtitle"],
            s["search_data"]["query"],
            s["search_data"]["form_data"]["data"]["category"]["str"]["value"],
            int(s["ad_count"]),
            s["probability"]
        ))
    return table
