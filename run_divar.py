import asyncio
import sys
from divar_function import Solve_Captcha

if len(sys.argv) < 3:
    print("Usage: python run_divar.py <token> <phone_number_owner>")
    sys.exit(1)

token = sys.argv[1]
phone_number_owner = sys.argv[2]

async def main():
    print(await Solve_Captcha(token, phone_number_owner))

asyncio.run(main())
