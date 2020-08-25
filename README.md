# mo-apiDataPull
Using Mozenda's API to put scraped data into a DataFrame

**Note: The API runs rather slow. 10+ Seconds per Request. Thus, I recommend looking at running only part of the code to validate the number of pages it will have to paginate through. If those number of pages is significantly high, the code will take an extended period of time to run.**

### Dependencies

Make sure you know your WebServiceKey and ViewID. You will use these to identify the data you are pulling in. Instructions on where to find these can be found here: https://help.mozenda.com/docs/en/generate-your-web-service-key

## Installing the Right Python Libraries

```
pip install pandas
pip install requests
```

## Code Walkthrough

```
import requests
import xml.etree.cElementTree as ET
import pandas as pd
```

These are the components of the libraries being imported in order to run this code. "requests" allows you to make a call to the Mozenda API and bring in that data. "xml.etree.cElementTree" is necessary in order to convert the xml file into a dataframe. "pandas" allows the user to manipulate and create a dataframe.

```
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
```

Here are the essentials to making the initial request to the Mozenda API. The WebServiceKey is a unique key that each Mozenda user has or can create in order to validate that they are who they say they are. This allows you to securely access your data. The ViewID identifies the specific data you are pulling from and the View you want. Headers are the key components for calling the API. The 'response' and xml_data creates a string with all of the data.

```
root = ET.fromstring(xml_data)

pageCount = root[3].text
```

The ET.fromstring converts the initial string into and "Element Tree" which allows you call specific components of the list. Root[3] identifies the number of total pages there are. This allows you to create an element to identify how many pages to paginate through.

```
while page <= pageCount:
...
i = 0

  while i < 1000:
```

This repeats the response call discussed above, but repeats for each page. i represents a line of data.

```
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

```

This final statement creates two lists: one for field names (columnslist) and one for value names (valueslist). It then iterates through each of the fields in the dataset. It identifies that there is a field name (the try-except statement) and then adds that field name to the columnslist and the value to the valueslist. It creates a new dataframe (df) if it's the very first iteration on the very first page. Otherwise, it creates df2 and appends it to the original df.

## Data Frame to SQL table

If you want to export this dataframe and add it to an existing database, check out my repository "Pandas Data Frame into a SQL Table".
