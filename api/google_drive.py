import pickle
import io
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def update_page(file_id, file_name):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)

    request = service.files().export(fileId=file_id, mimeType=f'text/html')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    with open(f'{file_name}.html', 'wb') as f:
        f.write(b'{% extends "base.html" %}\n')
        f.write(b'{% block body %}\n')
        f.write(fh.read())
        f.write(b'\n{% endblock body %}')
        f.close()

if __name__ == '__main__':
    update_page('1B8J_rQtCihzPVSN5wOf7SgEOQRlJFs5Rsf3wFH9_hwM', 'teaching_teacher')
    update_page('198UELcFM1OojGDVhEl5hk1vRXesDCa03vMldvA6HHGQ', 'machine_learning')
    update_page('1xgPgq4xDpvCS8Y4rkIYf2Gm_xXr0pg7-aEysidfR3-I', 'terminal')