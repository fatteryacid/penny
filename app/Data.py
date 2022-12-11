# ==================================================
import pandas as pd
import pendulum
import uuid

import pickle
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy import create_engine

# ==================================================
# Notes
'''
Scope:
    - extraction from source google sheets
    - preliminary data transformation for database insertion
    - load into staging environment
'''


# ==================================================
class Data():
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.df = None
        self.cred = None
        self.length = None

    def __repr__(self):
        return self.df.head(20)
    
    @property
    def size(self):
        return self.length
        
    def auth(self):
        #Checks for existing tokens
        if os.path.exists('./secret/secret_token.pickle'):
            with open('./secret/secret_token.pickle', 'rb') as token:
                self.cred = pickle.load(token)


        #Check for cred validity
        if not self.cred or not self.cred.valid:
            if self.cred and self.cred.expired and self.cred.refresh_token:
                self.cred.refresh(Request())

            else:
                scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
                flow = InstalledAppFlow.from_client_secrets_file('./secret/secret_client_secrets.json', scopes=scope)

                flow.run_local_server(port=5537, prompt='consent', authorization_prompt_message='')
                print('Reauthorization needed. Visit localhost:5537.')

                self.cred = flow.credentials

            #Writes token for future use
            with open('./secret/secret_token.pickle', 'wb') as f:
                pickle.dump(self.cred, f)
          
    def fetch(self, desired_range, headers):
        if not self.cred or self.cred is None:
            self.auth()

        try:
            service = build('sheets', 'v4', credentials=self.cred)

            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId = self.sheet_id,
                range = desired_range
            ).execute()

        except HttpError as error:
            print(f'An error occurred: {error}')
            return error
            
        if 'values' in result.keys():
            self.df = pd.DataFrame(result['values'], columns=headers)
            self.length = len(result['values']) - 1

        else:
            pass

    #Used to build UUIDs for data integrity and granularity
    def enrich(self, timezone):
        #Create UUIDs for each entry
        self.df['id'] = [uuid.uuid4() for _ in range(len(self.df.index))]
        self.df['extract_date'] = [pendulum.now(timezone).to_datetime_string() for _ in range(len(self.df.index))]


    #Deprecate this, will handle in dbt
    def prepare(self):
        #Process strings
        for i in self.df.columns:
            try:
                self.df[i] = self.df[i].str.lower()

                self.df[i] = self.df[i].str.replace("[@#%^$&*()']", '', regex=True)
                self.df[i] = self.df[i].str.strip()


                self.df[i] = self.df[i].str.replace('[-\s]', '_', regex=True)
                self.df[i] = self.df[i].str.replace('_{2,}', '_', regex=True)

            except TypeError:
                pass

        #Process amounts - remove accounting formatting
        temp = []
        
        for i in self.df.itertuples():
            j = str(i[3])
            
            if '(' in j and ')' in j:
                j = j.replace('(', '') 
                j = j.replace(')', '')
                j = '-' + j
                
            temp.append(j)
        
        self.df['amount'] = temp
        self.df['amount'] = pd.to_numeric(self.df['amount'])


    #Send to db
    def commit(self, engine_url, rel_name):
        if self.df.isnull().any().any():
            raise Exception('NullError')

        engine = create_engine(engine_url, echo=False)

        self.df.to_sql(
                name = rel_name, 
                con=engine,
                if_exists='append',
                index=False
            )
            

        engine.dispose()

    #Get head
    def peek(self):
        if self.df is None:
            return None
        else:
            return self.df.head()

    #Get tail  
    def peer(self):
        if self.df is None:
            return None
        else:
            return self.df.tail()
        
    