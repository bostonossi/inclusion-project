from sqlalchemy import create_engine
engine = create_engine('mysql://ghtorrent_user:ossd1-ght0rrent@128.31.27.157:33306/ghtorrent_restore')
connection = engine.connect()
result = connection.execute("select * from projects limit 5")
for row in result:
    print(row)
connection.close()