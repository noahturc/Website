from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from decimal import *
import pandas as pd
import json
import socket


socket.gethostname()

def extractfromconfig():
    try:
        # sql config
        global db
        global uid
        global passwd

        #ensure config.json is UTF-8.  Use Notepad to edit config.json
        print ("Opening Config.json")
        json_file=open(r"C:\Noah\gitProjects\publicNoahRepo\caseStudyWebsite\caseStudyPhotosAndData\case2\config.json","r",encoding='utf-8')

        print ("Loading Config.json")    
        data = json.load(json_file)

        print ("Assigning vals to sqlEntries")
        for r in data['sqlEntries']:
            if r['configvar'] == 'db':
                db=r['configval']
            if r['configvar'] == 'UserID':
                uid=r['configval']
            if r['configvar'] == 'Password':
                passwd=r['configval']

        print ("in extractfromconfig, db: " + db)
        print ("in extractfromconfig, uid: " + uid)
        print ("in extractfromconfig, passwd" + passwd)

        print ("Closing Config.json")
        json_file.close()                                   
    except Exception as e:
        print("Error extracting from config: " + str(e))                

def getPercentagePerformanceFromSQL():
    try:
        global s
        global strconn 
        global engine

        extractfromconfig()    

        '''Prior to running this code, Create a 64 bit ODBC System DSN with name as: NoahDSN
            Server as: Tropplt-Eturcas
            Default Database: MyTrace
            Trust Server Certificate: <checked>'''

        strconn = "mssql+pyodbc://" + uid + ":" + passwd + "@NoahDSN" #+ sqlsrvr + ":1433/" + db +"?driver=" + drivr +""
        
        engine = create_engine(strconn)
    
        Session = scoped_session(sessionmaker(bind=engine))
        s = Session()

        eSession = scoped_session(sessionmaker(bind=engine))       
        e = eSession()

        tSession = scoped_session(sessionmaker(bind=engine))       
        t = tSession()

        dSession = scoped_session(sessionmaker(bind=engine))       
        d = dSession()

        sql_query = text("select ymd, myPerc, dowPerc from vNoahCaseStudy2 Order by ymd")
        
#        src_Perf = s.execute(sql_query)
        df = pd.read_sql(sql_query, engine)
#        html_content = df.to_html(index=False)
        

        s.commit()
        s.close()
        e.commit()
        e.close()
        t.commit()
        t.close() 
        d.close()

        return df
 
    except Exception as e:
        print("THERE WAS AN ERROR")

if __name__ == "__main__":
   
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    df = getPercentagePerformanceFromSQL()
    print(df.head(), f"\n\n\nNumber of rows: {len(df)}\n")



#    df['ymd'] = pd.to_datetime(df['ymd'], format='%Y%m%d')



#    plt.figure(figsize=(10, 6))  # Optional: Set the figure size
#    plt.plot(df['ymd'], df['myPerc'], label='My Account')
#    plt.plot(df['ymd'], df['dowPerc'], label='Dow Jones')

#    plt.xlabel('Date')  # X-axis label
#    plt.ylabel('Percentage')  # Y-axis label
#    plt.title('Performance Of My Simulated Account vs Dow Jones')  # Title of the graph
#    plt.legend()  # Optional: Add a legend
#    plt.grid(True)  # Optional: Add a grid
#   plt.show()













    # Convert ymd column to datetime
    df['ymd'] = pd.to_datetime(df['ymd'], format='%Y%m%d')

    # Define the date where activity begins
    activity_start_date = pd.Timestamp('2024-02-13')

    # Plot the data
    plt.figure(figsize=(10, 6))  # Optional: Set the figure size
    plt.plot(df['ymd'], df['myPerc'], label='My Account')
    plt.plot(df['ymd'], df['dowPerc'], label='Dow Jones')

    # Configure plot
    plt.xlabel('Date')  # X-axis label
    plt.ylabel('Percentage')  # Y-axis label
    plt.title('Performance Of My Simulated Account vs Dow Jones')  # Title of the graph
    plt.legend()  # Add a legend
    plt.grid(True)  # Add a grid

    # Set the x-axis limits to start from the activity start date
    plt.xlim(left=activity_start_date)

    # Force 2024-02-13 to appear as a tick on the x-axis
    current_ticks = plt.xticks()[0]
    new_ticks = list(current_ticks) + [mdates.date2num(activity_start_date)]  # Convert date to numerical format
    plt.xticks(new_ticks, rotation=45)  # Add and rotate x-axis labels

    plt.show()