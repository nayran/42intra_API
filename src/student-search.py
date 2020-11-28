#!/usr/local/bin/python3


import requests
import sys
import os
import pandas as pd
from dotenv import load_dotenv
from utils import bytetodict
from utils import get_user_id
from utils import url_join
from utils import error
from utils import print_infos


# Funcao que requere a token, versao em python do cURL disponibilizado pelo API
# tambem faz o tratamento de dados para retornar somente a token
def get_token():
    load_dotenv()
    data = {
      'grant_type': 'client_credentials',
      'client_id': os.getenv("CLIENT_ID"),
      'client_secret': os.getenv("CLIENT_SECRET")
    }
    response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
    token = bytetodict(response.content)
    return token['access_token']


# Grava a token e user_id e define o header que sera enviado na requisicao,
# analisa erros de input, pega a flag recebida e define o endpoint para
# requisitar os dados do usuario. Converte a resposta do servidor em DataFrame
# e manda imprimir.
def student_search():
    token = get_token()
    headers = {'Authorization': 'Bearer %s' % token}
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        error('Invalid arguments')
    user_id = get_user_id(sys.argv[1], headers)
    if user_id is None:
        error('Not a valid user')
    if (len(sys.argv) == 3):
        flag = sys.argv[2]
    else:
        flag = None
    if (flag == 'staff'):
        flag = 'staff?'
    endpoint = '/users/%s/' % user_id
    url = url_join(endpoint)
    response = requests.get(url, headers=headers)
    response = bytetodict(response.content)
    if response == {}:
        error('Login not found')
    df = pd.Series(response)
    print_infos(df, flag)


def main():
    student_search()


if __name__ == "__main__":
    main()
