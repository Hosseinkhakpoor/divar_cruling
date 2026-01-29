import os,divar_function
from dotenv import load_dotenv
load_dotenv()
authorization=os.getenv("authorization")
phone_number_owner=os.getenv("phone_number_owner01")
token='gZn4ITPT'
#phon=divar_function.get_number(token=token,authorization=authorization)
#print(phon)
d=divar_function.serch_query('یدک کش',['715'])
print(d)