import requests,uuid,tabulate,time,subprocess
from playwright.async_api import async_playwright

def get_number(token,authorization):
    contact_uuid = str(uuid.uuid4())
    url=f'https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}'
    data={"contact_uuid":contact_uuid}
    headers={'authorization':authorization,
         "content-type":"application/json"}
    res=requests.post(url,json=data,headers=headers)
    js = res.json()
    if 'hip_action' in js:
        return {
            'status': 'SECURITY_BLOCK',
            'phone': None}

    if js.get('type') == 'BAD_REQUEST':
        return {
            'status': 'NOT_FOUND',
            'phone': None}

    if 'widget_list' in js:
        for widget in js['widget_list']:
            try:
                phone = widget['data']['action']['payload']['phone_number']
                return {
                    'status': 'SUCCESS',
                    'phone': phone
                }
            except KeyError:
                pass

        return {
            'status': 'LIMITED_SUCCESS',
            'phone': None}
    
    return {
        'status': 'UNKNOWN',
        'phone': None,
        'raw': js}

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


def divar_ads_exists(token):
    url = f"https://divar.ir/v/{token}"
    r = requests.get(url)
    if r.status_code == 200:
        return True
    return False


def cleanup_expired(conn, is_valid=divar_ads_exists):
    with conn.cursor() as cur:
        cur.execute("SELECT id, ads_link FROM derivers WHERE Phone_number = '' OR  Phone_number IS NULL")
        rows = cur.fetchall()

    expired_ids = []
    for row in rows:
        if not is_valid(row[1]):
            expired_ids.append(row[0])

    if not expired_ids:
        return 0

    with conn.cursor() as cur:
        cur.execute("DELETE FROM derivers WHERE id = ANY(%s)", (expired_ids,))
    conn.commit()
    return len(expired_ids)

def insert_over_search(conn,data_serch):
    with conn.cursor() as cur:
        for i in range (len(data_serch['tokens'])):
            token=data_serch['tokens'][i]
            city=data_serch['City'][i]
            query=f"INSERT INTO derivers (City,ads_Link) VALUES ( '{city}','{token}') ON CONFLICT (ads_Link) DO NOTHING RETURNING id, City, ads_Link;"
            try:
                cur.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("ERROR:", e)

def export_number(conn,authorization,phone_number_owner) :
    with conn.cursor() as cur:
        cur.execute("SELECT  ads_link FROM derivers WHERE Phone_number IS NULL OR Phone_number='' ;")
        rows = cur.fetchall()
        i=0
        for row in rows:
            token=row[0]
            ans=get_number(token,authorization)
            if ans['status']=='SUCCESS':
                i=i+1
                number_phon=ans['phone']
                try:
                    cur.execute(f"UPDATE derivers SET Phone_number='{number_phon}' WHERE ads_link='{token}'")
                    conn.commit()          
                except Exception as e:
                    conn.rollback()
                    print("ERROR:", e)
                    break
            elif ans['status']=='LIMITED_SUCCESS' or ans['status']=='NOT_FOUND':
                try:
                    cur.execute(f"DELETE FROM derivers WHERE ads_link='{token}';" )
                    conn.commit()          
                except Exception as e:
                    conn.rollback()
                    print("ERROR:", e)
                    break
            elif ans['status']=='SECURITY_BLOCK':
                try:
                    result = subprocess.run(
                    ["python", "run_divar.py", token, phone_number_owner],
                    capture_output=True,
                    text=True)
                    number_phon=result.stdout 
                    if '\n' in number_phon:
                        number_phon=number_phon.replace('\n','')
                    if'u' in number_phon:
                        print('User is closed window')
                        break
                    else:
                        print(number_phon)
                except:
                    print('Please solve CAPTCHA', f'\n token={token}')
                    break
                try:
                    cur.execute(f"UPDATE derivers SET Phone_number='{number_phon}' WHERE ads_link='{token}'")
                    conn.commit()   
                    i=i+1       
                except Exception as e:
                    conn.rollback()
                    print("ERROR:", e)
                    break
            else:
                print('Please check ',token,ans)
                break
        print(f'number of phon_number export = {i}')

async def Solve_Captcha(token,phone_number_owner):
    async with async_playwright() as p:
        context =await  p.chromium.launch_persistent_context(
            executable_path=r"C:\\Program Files\\Google\\Chrome\Application\\chrome.exe",
            user_data_dir=f"divar_profile\\{phone_number_owner}",
            headless=False,
            locale="fa-IR")
        page =await  context.new_page()
        await page.goto(f"https://divar.ir/v/{token}")
        await page.locator("button.post-actions__get-contact").click()
        try:
            await page.wait_for_selector("a[href^='tel:']", timeout=120000)
        except Exception as e:
            if "Target closed" in str(e) or "has been closed" in str(e):
                return 'u'
        phone_href = await page.locator("a[href^='tel:']").get_attribute("href")
        phone = phone_href.replace("tel:", "")
        return phone
    