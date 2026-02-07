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

def ads_export(quary,city,category,last_post_date='',layer_page=1,page=1,first_page_viewed_at='',search_uid=''):
    url='https://api.divar.ir/v8/postlist/w/search'
    data0={"city_ids": city,
            "source_view": "SEARCH",
            "disable_recommendation": "false",
            "map_state": {"camera_info": {"bbox": {}}},
            "search_data": {"form_data": {"data": {"category": {"str": {"value": category}}}},
                "server_payload": {
                "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                "additional_form_data": {"data": {"sort": {"str": {"value": "sort_date"}}}}},
                "query": quary}}
    data1={"city_ids": city,
            "source_view": "SEARCH",
            "pagination_data": {
                "@type": "type.googleapis.com/post_list.PaginationData",
                "last_post_date": last_post_date,
                "page": page,
                "layer_page": layer_page,
                "search_uid": search_uid,
                "first_page_viewed_at": first_page_viewed_at},
            "disable_recommendation": "false",
            "map_state": {"camera_info": {"bbox": {}}},
            "search_data": {
                "form_data": {
                "data": {"category": {"str": {"value": category}}}},
                "server_payload": {
                "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                "additional_form_data": {"data": {"sort": { "str": {"value": "sort_date"}}}}},
                "query":quary}}
    if last_post_date=='':
        data=data0
    else:
        data=data1
    headers={"content-type":"application/json",
             "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
    serche1=requests.post(url,json=data,headers=headers)
    tokens=[]
    City=[]
    if serche1.status_code != 200:
        print(f"Error: {serche1.status_code} - {serche1.text}")
        return []        
    for s in serche1.json()['list_widgets']:
        try:
            City.append(s["data"]["action"]["payload"]["web_info"]["city_persian"])
            tokens.append(s["data"]["action"]["payload"]["token"])
        except:
            pass
    serche_data={
        "last_post_date":serche1.json()['pagination']['data']['last_post_date'],
        "first_page_viewed_at": serche1.json()['pagination']['data']['first_page_viewed_at'],
        "layer_page":serche1.json()['pagination']['data']['layer_page'],
        "page":serche1.json()['pagination']['data']['page'],
        "search_uid":serche1.json()['pagination']['data']['search_uid'],
        "tokens": tokens,
        "City": City
    }
    return serche_data 

def ads_export_all(quary,city,category,number_of_ads=24):
    data_serch=ads_export(quary,city,category)
    last_post_date=data_serch['last_post_date']
    page=data_serch['page']
    layer_page=data_serch['layer_page']
    first_page_viewed_at=data_serch['first_page_viewed_at']
    search_uid=data_serch['search_uid']
    print(last_post_date)
    City=data_serch['City']
    tokens=data_serch['tokens']
    while len(tokens)<number_of_ads:
        time.sleep(5)
        data_serch=ads_export(quary,city,category,last_post_date,layer_page,page,first_page_viewed_at,search_uid)
        last_post_date=data_serch['last_post_date']
        print(last_post_date)
        City=City+data_serch['City']
        tokens=tokens+data_serch['tokens']
    searche_data={
        "tokens": tokens,
        "City": City
    }
    return searche_data