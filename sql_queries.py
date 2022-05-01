import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS part songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
        artist        VARCHAR(MAX) NOT NULL,
        auth          VARCHAR(MAX) NOT NULL,
        firstName     VARCHAR(MAX) NOT NULL,
        gender        CHAR ,
        itemInSession INT NOT NULL,
        lastName      VARCHAR(MAX) ,
        length        double precision,
        level         VARCHAR (MAX) NOT NULL,
        location      VARCHAR (MAX) ,
        method        VARCHAR (MAX) NOT NULL ,
        page          VARCHAR (MAX) NOT NULL,
        registration  NUMERIC (MAX) ,
        sessionId     INT (MAX) NOT NULL,
        song          VARCHAR (MAX) NOT NULL,
        status        INT (MAX) NOT NULL,
        ts            timestamp NOT NULL,
        userAgent     VARCHAR (MAX) ,
        userId        INT (MAX) NOT NULL);
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
   song_id          varchar(max) NOT NULL,
    title           VARCHAR(max),
    duration        numeric,
    year            int NOT NULL,
    artist_id varchar(max) NOT NULL,
    artist_name      varchar(max) ,
    artist_latitude  double precision,
    artist_longitude double precision,
    artist_location  varchar(max),
     num_songs int  
);
""")


songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
                            (songplay_id IDENTITY(0,1) PRIMARY KEY,
                            start_time timestamp NOT NULL, 
                            user_id int NOT NULL,
                            level varchar, 
                            song_id varchar,
                            artist_id varchar,
                            session_id int,
                            location varchar,
                            user_agent varchar
                            );
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users
                        (user_id int PRIMARY KEY,
                        first_name varchar,
                        last_name varchar,
                        gender char,
                        level varchar
                        );
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs
                         (song_id varchar PRIMARY KEY,
                         title varchar NOT NULL,
                         artist_id varchar,
                         year int,
                         duration numeric NOT NULL);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                          (artist_id varchar PRIMARY KEY,
                          name varchar NOT NULL,
                          location varchar,
                          latitude double precision,
                          longitude double precision);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table 
                        (start_time timestamp PRIMARY KEY,
                         hour int,
                         day int,
                         week int,
                         month int,
                         year int,
                         weekday int);
""")

# STAGING TABLES

staging_events_copy = ("""Copy staging_events's3://udacity-dend/log_data'
    credentials 'aws_iam_role={}'
    format as json 's3://udacity-dend/log_json_path.json'
    region 'us-west-2'
""".format(ARN)

staging_songs_copy = ("""copy staging_songs from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role={}'
   JSON AUTO region 'us-west-2'
""".format(ARN)
                       


# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays 
                            (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT se.ts, se.userid, se.level, ss.song_id, ss.artist_id, se.sessionid, se.location, se.useragent
                            FROM staging_events se
                            JOIN staging_songs ss
                            ON se.artist = ss.artist_name 
                            where se.page = 'NextSong'
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT(se.userId), se.firstName, se.lastName, se.gender, se.level
    FROM staging_events se
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT(ss.song_id), ss.title, ss.artist_id, ss.year, ss.duration 
    FROM staging_songs ss
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT(ss.artist_id), ss.artist_name, ss.artist_location, ss.artist_latitude, ss.artist_longitude
    FROM staging_songs ss
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT distinct sp.start_time, extract(hour from sp.start_time), extract(day from sp.start_time), extract(week from sp.start_time), extract(month from sp.start_time), extract(year from sp.start_time), extract(dayofweek from sp.start_time)
    FROM songplays sp
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

                      
                      


