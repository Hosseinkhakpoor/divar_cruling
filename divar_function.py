import requests,uuid,tabulate,time
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
    if res.status_code==200:
        authorization=f"Basic {res.json()['token']}"
    else:
        authorization='Basic '
    return authorization

def serch_query(quary,city):
    url='https://api.divar.ir/v8/prediction/w/query'
    data={"query":quary,"cities":city}
    headers={"content-type":"application/json"}
    serche0=requests.post(url,json=data,headers=headers)
    if serche0.status_code != 200:
        return []
    t = []
    for s in serche0.json()["suggestions"]:
        t.append((
            s["title"],
            s["subtitle"],
            s["search_data"]["query"],
            s["search_data"]["form_data"]["data"]["category"]["str"]["value"],
            int(s["ad_count"]),
            s["probability"]
        ))
    headers = ["title", "subtitle","query","value","ad_count","probability"]
    table=tabulate.tabulate(t, headers=headers, tablefmt="grid")
    return table

def ads_export(quary,city,category,last_post_date=''):
    url='https://api.divar.ir/v8/postlist/w/search'
    data={"city_ids":city,
          "last_post_data": last_post_date,
       "source_view":"SEARCH_BAR_QUERY_SUGGESTION",
       "disable_recommendation":'false',
       "map_state":{"camera_info":{"bbox":{}}},
       "search_data":{"form_data":{"data":{"category":{"str":{"value":category}}}},
                      "server_payload":{"@type":"type.googleapis.com/widgets.SearchData.ServerPayload",
                                        "additional_form_data":{"data":{"sort":{"str":{"value":"sort_date"}}}}},
                                        "query":quary}}
    headers={"content-type":"application/json"}
    serche1=requests.post(url,json=data,headers=headers)
    tokens=[]
    City=[]
    for s in serche1.json()['list_widgets']:
        try:
            City.append(s["data"]["action"]["payload"]["web_info"]["city_persian"])
            tokens.append(s["data"]["action"]["payload"]["token"])
        except:
            pass
    serche_data={
        "last_post_date":serche1.json()['pagination']['data']['last_post_date'],
        "tokens": tokens,
        "City": City
    }
    return serche_data 

def ads_export_all(quary,city,category,number_of_ads=24):
    data_serch=ads_export(quary,city,category,last_post_date='')
    last_post_date=data_serch['last_post_date']
    City=data_serch['City']
    tokens=data_serch['tokens']
    while len(tokens)<number_of_ads:
        time.sleep(5)
        data_serch=ads_export(quary,city,category,last_post_date)
        last_post_date=data_serch['last_post_date']
        City=City+data_serch['City']
        tokens=tokens+data_serch['tokens']
    searche_data={
        "tokens": tokens,
        "City": City
    }
    return searche_data