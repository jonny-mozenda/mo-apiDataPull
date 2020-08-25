import requests
import xml.etree.cElementTree as ET
import pandas as pd


url = "https://api.mozenda.com/rest"

WebServiceKey = #"WebServiceKey"
ViewID = #"ViewID"

querystring = {"WebServiceKey":WebServiceKey,"Service":"Mozenda10","Operation":"View.GetItems","ViewID":ViewID,"PageItemCount":"1000","PageNumber":"1"}

headers = {
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "api.mozenda.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

xml_data = response.text

root = ET.fromstring(xml_data)

pageCount = int(root[3].text)

page = 1

while page <= pageCount:

    url = "https://api.mozenda.com/rest"

    querystring = {"WebServiceKey":"6B8ACEC8-6327-4DD6-97BE-5BE6261C28B7","Service":"Mozenda10","Operation":"View.GetItems","ViewID":"1076","PageItemCount":"1000","PageNumber":page}

    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "6e865eef-68f9-44b6-8c7b-02202a8f462b,47411ebc-b32e-457e-a874-652ecee93072",
        'Host': "api.mozenda.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    xml_data = response.text

    root = ET.fromstring(xml_data)

    i = 0

    while i < 1000:

        columnslist = []
        valueslist = []

        for x in root[4][i].iter():

            try:
                x.tag
            except Exception:
                break

            colName = x.tag
            columnslist.append(colName)

            valName = x.text
            valueslist.append(valName)

        if page == 1 and i == 0:
            df = pd.DataFrame([valueslist], columns = columnslist)

        else:
            df2 = pd.DataFrame([valueslist], columns = columnslist)
            df = df.append(df2)

        i = i + 1

    page = page + 1
df
