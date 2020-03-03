from sqlalchemy import *
import simplejson as json

with open('config/ossdi.config.json') as config_file:
    config_data = json.load(config_file)

username = config_data['Ossdi']['user']
password = config_data['Ossdi']['pass']
hostname = config_data['Ossdi']['host']
portname = config_data['Ossdi']['port']
dbname = config_data['Ossdi']['name']
connection_string ='mysql://'+username+':'+password+'@'+hostname+':'+portname+'/'+dbname

engine = create_engine(connection_string)
connection = engine.connect()
result = connection.execute("select * from projects limit 5")
for row in result:
    print(row)
connection.close()