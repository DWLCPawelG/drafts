"""Basic SQLAlchemy example - SELECTing everything from some table"""
import datetime

from sqlalchemy import create_engine, Table, MetaData, func, Integer, String, Column, ForeignKey
from sqlalchemy.sql import select, or_, and_, not_

if __name__ == "__main__":
    # 4 lines necessity
    engine = create_engine('sqlite:///chinook.db', echo=True)
    meta = MetaData()
    meta.reflect(bind=engine)
    connection = engine.connect()

    # print all tables in DB:
    table_names = engine.table_names()
    print(table_names)

    # define tables or load tables definitions
    albums = Table('albums', meta, autoload=True, autoload_with=engine) # or albums = meta.tables['albums'] (see lower)

    # create basic query. The one here is equivalent to "SELECT * FROM artists".
    select_all_albums = select([albums])
    # this prints sql query: "SELECT albums."AlbumId", albums."Title", albums."ArtistId" FROM albums
    print(select_all_albums)
    # this prints all 3 column values with 10 spaces indentation for album_id
    for album_id, title, artist_id in connection.execute(select_all_albums):
        print(f'{album_id:10} - {title} - {artist_id}')

    # check Column names in a table:
    for column in albums.c:
        print(f'{column.name} {column.type}')

    # access only certain column: table_name.c.columnn_name
    for row in connection.execute(select_all_albums):
        print(row[albums.c.AlbumId], ": ", row[albums.c.Title])

    artists = meta.tables['artists']
    tracks = meta.tables['tracks']
    albums = meta.tables['albums']
    genres = meta.tables['genres']
    employees = meta.tables['employees']
    customers = meta.tables['customers']
    invoice_items = meta.tables['invoice_items']
    invoices = meta.tables['invoices']
    media_types = meta.tables['media_types']
    playlist_track = meta.tables['playlist_track']
    playlists = meta.tables['playlists']
    sqlite_sequence = meta.tables['sqlite_sequence']
    sqlite_stat1 = meta.tables['sqlite_stat1']

    # conditional queries:
    for row in connection.execute(select([albums]).where(albums.c.AlbumId < 10)):
        print(f'{row[albums.c.Title]}: {row[albums.c.ArtistId]}')
    # condtional with datetime.datetime()
    for row in connection.execute(select([invoices]).where(invoices.c.InvoiceDate > datetime.datetime(2011, 12, 31))):
        print(row[invoices.c.BillingCity])
    # conditional with .like:
    for row in connection.execute(select([employees]).where(employees.c.Title.like('%Manager'))):
        print(row[employees.c.FirstName], row[employees.c.LastName])

    # or_
    for row in connection.execute(select([tracks]).where(or_(tracks.c.Composer.like('%Joe Perrry%'), tracks.c.Composer.like('%Steven Tyler%')))):
        print(row[tracks.c.Name])

    for row in connection.execute(select([customers]).where(or_(customers.c.Country.like('United Kingdom'), customers.c.Country.like('Poland')))):
        print(f'{row[customers.c.CustomerId]}. {row[customers.c.FirstName]} {row[customers.c.LastName]} {row[customers.c.Country]}')

    # and_
    for row in connection.execute(select([customers]).where(and_(customers.c.Country.like('France'), customers.c.City.like('Paris')))):
        print(f'{row[customers.c.CustomerId]}. {row[customers.c.FirstName]} {row[customers.c.LastName]} {row[customers.c.City]}')

    # not_ (with and_)
    for row in connection.execute(select([customers]).where(and_(not_(customers.c.Country.like('France')), (not_(customers.c.Country.like('Canada')))))):
        print(f'{row[customers.c.CustomerId]}. {row[customers.c.FirstName]} {row[customers.c.LastName]} {row[customers.c.Country]}')

    # selecting only specific columns instead of whole tables, with limit applied at the end
    query = select([customers.c.FirstName, customers.c.LastName, customers.c.City, customers.c.Country]).limit(10)
    for first_name, last_name, city, country in connection.execute(query):
        print(f'{first_name} {last_name} from {city}, {country}')

    # sorting ascending:
    query = select([tracks.c.Name, tracks.c.Milliseconds]).order_by(tracks.c.Milliseconds).limit(10)
    for track, time in connection.execute(query):
        print(f'{track} is {time} milliseconds long')

    # sorting descending
    query = select([tracks.c.Name, tracks.c.Milliseconds]).order_by(tracks.c.Milliseconds.desc()).limit(10)
    for track, time in connection.execute(query):
        print(f'{track} is {time} milliseconds long')

    # join = select.from(table_left.join(table_right))
    query = select([customers.c.FirstName, customers.c.LastName, invoices.c.BillingAddress])\
            .select_from(invoices.join(customers))
    for first_name, last_name, address in connection.execute(query):
        print(f'{first_name} {last_name} from {address}')
    # 2
    query = select([artists.c.Name, albums.c.Title]).select_from(artists.join(albums))
    for name, title in connection.execute(query):
        print(f'{name}: {title}')

    # INSERT: connection.execute(<table.name>.insert(), <column_name>=<inserted_value>)
    insert = connection.execute(media_types.insert(), Name='Whatever')
    query = select([media_types.c.MediaTypeId, media_types.c.Name])
    for Id, Name in connection.execute(query):
        print( f'{Id}: {Name}')

    # INSERT with not all column values will:
    # - FAIL if all NOT NULL columns are not filled
    # - SUCCEED if all NOT NULL columns are filled, adding NULL to rest of unfilled columns
    insert_track = connection.execute(tracks.insert(), Composer='Pablo', Name='I\'m hungry', MediaTypeId=1, Milliseconds=1, UnitPrice=0.99)

    # INSERT multiple rows: insert rows as a list of dictionaries:
    # connection.execute(<table_name>.insert(), [{'FirstName': 'John', 'LastName': 'Adams'},
    #                                                                   {'FirstName': 'Amy', 'LastName': 'Klein'}])
    insert_multiple_tracks = connection.execute(tracks.insert(), [{'Composer': 'Some Guy', 'Name': 'Some Title', 'MediaTypeId': 1, 'Milliseconds': 2, 'UnitPrice': 2},
                                                                  {'Composer': 'Another One', 'Name': 'A Song', 'MediaTypeId': 2, 'Milliseconds': 33333333, 'UnitPrice': 4}])

    # UPDATE row - be sure to include .where() clause - if not UPDATE will affect EVERY row in table
    # connection.execute(<table_name>.update(),where(<condition>).values(<column_name>=<new_value>
    update_single_track = connection.execute(tracks.update().where(tracks.c.TrackId <= 3506).values(Name='LOL'))
    update_single_track_with_and_condition = connection.execute(tracks.update().where(and_(tracks.c.TrackId >= 3504, tracks.c.TrackId <= 3506)).values(GenreId=8)) # with and_ condition

    # DELETE row - be sure to include .where() clause - if not DELETE will affect EVERY row in table
    # connection.execute(<table_name>.delete().where(<table_name>.c.<column_name> >= 26)
    delete_from_tracks = connection.execute(tracks.delete().where(tracks.c.TrackId >= 3533))

    # GROUP_BY with func.count()
    group_by_query = select([artists.c.Name, func.count(albums.c.Title)]).select_from(albums.join(artists)).group_by(albums.c.ArtistId)
    for name, number in connection.execute(group_by_query):
        print(f'{name}: {number} albums')

    # GROUP_BY with func.avg() and order_by().desc() - you're getting the hang of it :-)
    gruop_by_with_avg = select([customers.c.FirstName, customers.c.LastName, func.avg(invoices.c.Total)]).select_from(customers.join(invoices)).group_by(invoices.c.CustomerId).order_by(func.avg(invoices.c.Total).desc()).limit(5)
    for first_name, last_name, number in connection.execute((gruop_by_with_avg)):
        print(f'{first_name} {last_name} spends average {number} per order')

    # TU SKOŃCZYŁEŚ

    # GROUP BY clause is specified by group_by method.
    # The below query is roughly equivalent to
    # SELECT Title, SUM(UnitPrice) as Price
    # FROM Albums
    # JOIN Tracks ON Albums.AlbumId = Tracks.AlbumId GROUP BY albums.AlbumId
    # LIMIT 5
    # query = (select([albums.c.Title, func.sum(tracks.c.UnitPrice).label('Price')])
    #          .select_from(albums.join(tracks))
    #          .group_by(albums.c.AlbumId)
    #          .limit(5))


