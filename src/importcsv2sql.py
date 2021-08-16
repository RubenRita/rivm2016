import pandas as pd
import sqlite3
import os
from dbutil import CreateDB

from pandas.io.pytables import dropna_doc



def data_obj(name):
    try:
        file_name = os.path.join(os.path.dirname(__file__), '..','data', name)    
    except:
        print ("No file!")    
    return file_name

def getIndicatores(csvFileName):
    '''
        Get all indicatores data from first row
        Split the ones with colon 
        DH will get the unit values       
    ''' 
    print(f'Get Indicatores {csvFileName}')  
    df = pd.read_csv(data_obj(csvFileName),sep=',',header=0)
    df.dropna(how='all', axis=1, inplace=True)
    dh = pd.read_csv(data_obj(csvFileName),sep=',' ,header=0, skiprows=1).columns.tolist()         
    list_of_indicators = []
    n = 1
    for record in df:
        if ':' in record:
            a = record.split(':')
            if len(a) == 3:
                dict = {'method':a[0],'category':a[1],'indicator':a[2],'unit':dh[n]}
                list_of_indicators.append(dict)
        n +=1
          
    return list_of_indicators       

   
def getEntries(csvFileName):
    '''       
       Get all the entries from csv
       Split the word in ,
       Get all units 
    '''
    print(f'Reading {csvFileName}')
    df = pd.read_csv(data_obj(csvFileName),sep=',',header=1)
    df = df.iloc[:, [1,2]]
    list_of_entries = []    
    for rows in df.values:
        if ',' in rows[0]:
            a = rows[0].split(',')
            if len(a) == 4:
                dict = {'product_name':a[0],'geography':str(a[1]).strip(' []'),'method':a[2],'data_source':a[3] ,'unit':rows[1]}
                list_of_entries.append(dict)
                
    return list_of_entries

def getImpacts(csvFileName):
    '''
        Get all impacts from csv file
        Get entry_id counting index and get 
        array with all impacts
    '''
    print(f'Reading {csvFileName}')
    df = pd.read_csv(data_obj(csvFileName),sep=',',header=0)
    i = 0
    list_of_impacts = []    
    for rows in df.values:
        if ',' in str(rows[1]):
            dict = {'entries_id': i,'coefficient': rows}
            list_of_impacts.append(dict)
        i += 1
        
    generator = ( item['coefficient'] for item in list_of_impacts)
    k = 1    
    list_complete = []
    for datos in generator:
        j = 1
        datos = list(datos)
        del datos[0:5]
        for dato in datos:            
            if not 'nan' in str(dato):
                dict = {'entries_id': k, 'indicator_id': j, 'coefficient': dato}
                list_complete.append(dict)                
            j+=1
        k+=1       
    return list_complete



def create_tables_insert_data(list_of_data,process_name):
    insert_data = CreateDB()      
    if process_name == 'indicators':
        insert_data.insert_indicators(list_of_data)
    elif process_name == 'entries':
        insert_data.insert_geographies()
        insert_data = CreateDB() 
        insert_data.insert_entries(list_of_data)
    elif process_name == 'impacts':
        insert_data.insert_impacts(list_of_data)


def main():
    csvFileName = "rivm2016.csv"
    #Create IndicatoresTable
    
    lista1 = getIndicatores(csvFileName)    
    create_tables_insert_data(lista1,"indicators")
    
    lista2 = getEntries(csvFileName)
    create_tables_insert_data(lista2,"entries")
    
    lista3=getImpacts(csvFileName)
    create_tables_insert_data(lista3,"impacts")

 
if __name__ == '__main__':
    main()