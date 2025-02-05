import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
column=["Food Name", "Drink or Food", "Food Serving Size","Energy Density"]
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "data/secretKey.json"
SPREADSHEET_ID = "  " #https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit?gid=0#gid=0
RANGE_NAME = "sheetName!D5:G332"  # Adjust as needed

def get_google_sheets_data(type = "read", writelist = None):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    if(type=="read"):
        service = build("sheets", "v4", credentials=creds) #Is used to initialize the API to make request
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        data = result.get("values", [])


        # Save data locally
        df = pd.DataFrame(data, columns=column)
        df.to_csv("data/local_data.csv" ,index=False)
        print("Data saved locally.")
        return df

    else:
        # Authenticate with Google Sheets
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

        # Open the Google Sheet by name
        spreadsheet = gc.open("Contacted Records")

        # Select a worksheet (by name or index)
        worksheet = spreadsheet.worksheet("Qualtrics Contact Info")  # Or use spreadsheet.get_worksheet(0)
        worksheet.append_rows(writelist)


def read_local_data():
    return pd.read_csv("data/local_data.csv")

# Use local data if it exists, otherwise fetch from API

# Reading values from Master Food List google sheets 
try:
    df = read_local_data()
    print("Using cached data.")
except FileNotFoundError:
    df = get_google_sheets_data("read")

print(df.head())

#Saving the required kCal info from Aramark in a csv file
extract_df = pd.read_csv("data/local_data.csv")
missing_calorie = []
print("Extracted data info: " , extract_df.info())

for missing in range(extract_df.shape[0]):
    if (str(extract_df.iloc[missing, 3]).endswith("?")):
        #extract_df.iloc[missing, 3] = ""
        extract_df.iloc[missing,3] = ""
        extract_df.iloc[missing,1:4] = extract_df.iloc[missing,1:4].replace('??', "")
        missing_calorie.append(extract_df.iloc[missing ,:].tolist())

missing_info = pd.DataFrame(missing_calorie, columns= column)
missing_info.to_csv("data/Required_kCal.csv", index=False)


# Writing values
data = pd.read_csv("data/pre_screener.csv", delimiter=",")
#data.dropna(axis = 0, how = 'all', inplace = True)
extract_df = data.loc[~data.drop(columns=["RecordedDate", "Finished"]).isna().all(axis=1)]
extract_df = extract_df.reset_index(drop=True)
extract_df.tail()

remaining_list = []
for rows in range(3):
    remaining_list.append(extract_df.iloc[(167 + rows), :].replace({np.nan: ""}).tolist())
    
print(type(remaining_list[0]))  # Check the data type
print(remaining_list[0])  # See the actual structure
get_google_sheets_data("write", remaining_list)