#!/usr/bin/env python3
"""
Gmail OAuth Authentication
Gera token de acesso para leitura de emails.
Executar uma vez localmente para gerar o token.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopo: apenas leitura de emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Gera ou atualiza token de acesso."""
    creds = None
    
    # Verifica se já existe token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não existe ou expirou, gera novo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Token expirado. Renovando...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Falha ao renovar token: {e}")
                print("Token foi revogado. Iniciando nova autenticação...")
                creds = None

        if not creds:
            print("Gerando novo token...")
            print("Uma janela do navegador vai abrir para autorização.")
            print()
            
            if not os.path.exists('credentials.json'):
                print("ERRO: Arquivo credentials.json não encontrado!")
                print("Coloque o arquivo credentials.json na raiz do projeto.")
                return
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Salva o token para próximas execuções
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        print()
        print("✅ Token gerado com sucesso!")
        print("Arquivo salvo: token.json")
    else:
        print("✅ Token válido encontrado!")

if __name__ == '__main__':
    main()