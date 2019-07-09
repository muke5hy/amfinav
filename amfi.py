import requests
import json
import boto3
import time
import pandas as pd 
import os

def month_range():
    result = []
    today = datetime.date.today()
    today = datetime.date(2019, 12, 1)    
    current = datetime.date(2019, 1, 1)    

    while current <= today:
        result.append([current, ((current + relativedelta(months=1))-relativedelta(days=1))])
        current += relativedelta(months=1)
    return result

class Amfi():
    def get_txt(self):
        resp = requests.get(self.url)
        if resp.status_code == 200:
            return resp.text
        else:
            print("Error in request", resp.status_code, resp.reason)
    
    def get_nav_daily(self):
        schemes = []
        lines = self.txt.split("\r\n")
        for line in lines:
            if len(line) > 0 and line[0] >= '0' and line[0] <= '9':
                items = line.split(";")
                if items[1].strip('-'):
                    schemes.append({
                        'code': items[0],'isin':items[1], 'name': items[3], 'nav': items[4], 'date': items[5]
                    })
                if items[2].strip('-'):
                    schemes.append({
                        'code': items[0],'isin':items[2],'name': items[3], 'nav': items[4], 'date': items[5]
                    })
        return schemes
    
    def get_nav_history(self):
        schemes = []
        lines = self.txt.split("\n")
        for line in lines:
            if len(line) > 0 and line[0] >= '0' and line[0] <= '9':
                items = line.split(";")
                
                if items[2].strip():
                    schemes.append({
                            'code': items[0],'isin':items[2], 'name': items[1], 'nav': items[4], 'date': items[7]
                    })
                if items[3].strip():
                    schemes.append({
                        'code': items[0],'isin':items[3], 'name': items[1], 'nav': items[4], 'date': items[7]
                    })
        return schemes
    
    def get_df(self, schemes):
        return pd.DataFrame(self.schemes)
    
    def download_schemes():
        url = "http://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0"
        r = requests.get(url)  
        with open("schemes.csv", 'wb') as f:
            f.write(r.content)

    
def download_history():
    months = month_range()
    for m in months:
        url = "http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={}&todt={}".format(m[0].strftime('%d-%b-%Y'),m[1].strftime('%d-%b-%Y'))
        path = "{}.txt".format(m[0].strftime('%Y%m'))
        if os.path.isfile(path):
            continue 
        r = requests.get(url)  
        with open(path, 'wb') as f:
            f.write(r.content)
        
def convert_to_csv():
    files = []
    with os.scandir('amfitxt') as i:
        for entry in i:
            if entry.is_file() and ".txt" in entry.name:
                files.append(entry.name)

    for file in files:
        with open('amfitxt/'+file) as f:
            amfi = Amfi()
            amfi.txt = f.read()
            schemes = amfi.get_nav_history()
            df = amfi.get_df(schemes)
            
        if not df.empty:
            name = file.replace('.txt', '.csv')
            df.to_csv("amficsv/"+name)


# url = "https://www.amfiindia.com/spages/NAVAll.txt"
# amfi = Amfi()
# data = amfi.get_txt().get_nav_history()
# data = amfi.get_txt().get_nav_daily()
