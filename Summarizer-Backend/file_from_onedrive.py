import requests
# Function to get file content from OneDrive
def get_file_content(site_id,drive_id,item_id,token):


    headers = {
        'Authorization': f'Bearer {token}'
    }
    file_content_endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{item_id}/content'
    response = requests.get(file_content_endpoint, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None