import requests
import streamlit as st


# Predefined credentials



def get_access_token(tenant_id, client_id, client_secret):
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    scope = 'https://graph.microsoft.com/.default'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
    }
    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get('access_token')
    return token


# Function to list items in the "Recordings" folder
def list_items_in_folder(site_id, drive_id, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    list_items_endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/Recordings:/children'
    response = requests.get(list_items_endpoint, headers=headers)
    if response.status_code == 200:
        items = response.json().get('value', [])
        return items
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return []


# Function to get file content from OneDrive
def get_file_content(site_id, drive_id, item_id, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    file_content_endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{item_id}/content'
    response = requests.get(file_content_endpoint, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None