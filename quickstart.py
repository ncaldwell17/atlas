# stuff to access the Google API client
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def retrieve_values(sheet_id, sheet_range):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    return result.get('values', [])


def create_df_with_first_row_headers(set_of_values):
    _df = pd.DataFrame(set_of_values)

    # replaces first row of DataFrame with the headers b/c it's not automatic
    headers = _df.iloc[0]
    _df = _df[1:]
    _df.columns = headers

    return _df


# returns a google spreadsheet converted to a pandas DataFrame
def retrieve_values_as_dataframe(_id, _range):
    return create_df_with_first_row_headers(retrieve_values(_id, _range))


