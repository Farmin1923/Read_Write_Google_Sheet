# Read_Write_Google_Sheet
The script will help to read and write value from google sheets. 

For reading or writing values from google excel sheet using python API:

[1] Create a new project in Google Developer Console: https://console.cloud.google.com/welcome?project=adept-portal-449919-a0 \\
[2] Enable the APIs from “Library”. \\
[3] Enable Google Sheets API, and Google Drive API. \\
[4] Create credentials, “Service accounts” for using the API key. \\
[5] By clicking the created credentials, click the “Keys”. \\
[6] Create a key, a json file consisting of the API key will be downloaded. \\
[7] In the json file, there is “client email:”. Copy it, and access this email in your google sheet. \\

# Required python library
gspread, oauth2client, and PyOpenSSL


