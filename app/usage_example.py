import os

from modules import bling, redis_client
from config import ConfigSingleton

def get_tokens_from_bling_using_code_in_url(code):

    bling.BlingApiTokenHandler().get_token_using_code(code)
    
    
def usage_example():
        
    bling.BlingApiTokenHandler().refresh_tokens(
    bling.TokenStorage.retrieve_token_by_key('refresh_token'))

    access_token = bling.TokenStorage.retrieve_token_by_key('access_token')
    refresh_token = bling.TokenStorage.retrieve_token_by_key('refresh_token')
    
    print('access_token: ', access_token)
    print('refresh_token: ', refresh_token)
    
    if access_token:
        # YOUR API CALLS HERE
        """
            headers = {'Authorization': f'Bearer {access_token}'}
            request = requests.Session()
            resp = request.get(url, headers=headers)
            ...
            ...
            data = resp.json()
            return data"""
        print('Example success')
        pass
    
if __name__ == '__main__':
    
    credentials_folder = os.path.join(os.getcwd(), 'credential')
    
    first_time_runing = not os.path.exists(credentials_folder)
    
    if first_time_runing:
        code = input('Code: ')
        get_tokens_from_bling_using_code_in_url(code)
    else:
        usage_example()

