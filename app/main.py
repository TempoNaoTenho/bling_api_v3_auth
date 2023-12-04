import os

from modules import bling
from app.usage_example import bling_api_call_example, get_tokens_with_code_example

def main():
    
    token_handler = bling.BlingApiTokenHandler()
    token_storage = bling.TokenStorage()
    
    credentials_folder = os.path.join(os.getcwd(), 'credential')
    first_time_runing = not os.path.exists(credentials_folder)
        
    if first_time_runing:
        code = input('Url redirection code: ')
        get_tokens_with_code_example(code, token_handler)
    else:
        api_call = bling_api_call_example(token_storage, token_handler)
        print(api_call)
        
if __name__ == '__main__':
    main()