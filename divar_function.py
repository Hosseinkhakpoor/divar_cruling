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
authorization="Basic eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJlYzExZmMyYS0zNTUyLTRjZDktYmU2OS1jNTQ4OTY5NmM2NjgiLCJ1aWQiOiIxMjUwZTJlNS01M2UyLTQxYjktOWQ1YS0wNmE0ZGRjNGQxY2QiLCJ1c2VyIjoiMDkxMjQxMzg1MzMiLCJ2ZXJpZmllZF90aW1lIjoxNzY3NzA2NDM1LCJpc3MiOiJhdXRoIiwidXNlci10eXBlIjoicGVyc29uYWwiLCJ1c2VyLXR5cGUtZmEiOiLZvtmG2YQg2LTYrti124wiLCJleHAiOjE3NzAyOTg0MzUsImlhdCI6MTc2NzcwNjQzNX0.8vZ0WdUl8N6BF6dcahSn0BqTz0nLEX-ttKaUmE74vYo"
token='gZn4ITPT'
phon=get_number(token=token,authorization=authorization)
print(phon)