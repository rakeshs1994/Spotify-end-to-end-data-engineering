create or replace database spotify;

CREATE or replace  TABLE spotify.PUBLIC.album_data(
  album_id string, 
  album_name string, 
  album_release_date string, 
  album_total_tracks INT, 
  album_url string);

CREATE OR replace TABLE spotify.PUBLIC.artist_data(
  artist_id string, 
  artist_name string, 
  external_url string);


CREATE OR REPLACE  TABLE spotify.PUBLIC.songs_data(
  song_id string, 
  song_name string, 
  duration_ms INT, 
  url string, 
  popularity INT, 
  song_added string, 
  album_id string, 
  artist_id string);


create or replace stage  spotify.PUBLIC.aws_stage_album
URL = "s3://spotify-etl-project-rakeshs/transformed_data/album_data/"
CREDENTIALS = (AWS_KEY_ID = '***' AWS_SECRET_KEY = '***');



COPY INTO spotify.PUBLIC.album_data
FROM '@spotify.PUBLIC.aws_stage_album/album_transformed_2025-09-10 16:53:11.318964.csv'
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

select * from spotify.PUBLIC.album_data;

TRUNCATE TABLE spotify.PUBLIC.album_data;


create or replace stage  spotify.PUBLIC.aws_stage_artist
URL = "s3://spotify-etl-project-rakeshs/transformed_data/artist_data/"
CREDENTIALS = (AWS_KEY_ID = '***' AWS_SECRET_KEY = '***');


COPY INTO spotify.PUBLIC.artist_data
FROM '@spotify.PUBLIC.aws_stage_artist/artist_transformed_2025-09-10 16:53:11.453740.csv'
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);


select * from spotify.PUBLIC.artist_data;

TRUNCATE TABLE spotify.PUBLIC.artist_data;


create or replace stage  spotify.PUBLIC.aws_stage_songs
URL = "s3://spotify-etl-project-rakeshs/transformed_data/songs_data/"
CREDENTIALS = (AWS_KEY_ID = '***' AWS_SECRET_KEY = '***');


COPY INTO spotify.PUBLIC.songs_data
FROM '@spotify.PUBLIC.aws_stage_songs/songs_transformed_2025-09-10 16:53:10.894851.csv'
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

select * from spotify.PUBLIC.songs_data;

TRUNCATE TABLE spotify.PUBLIC.songs_data;


create or replace storage  integration spotify_init
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER =S3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::386454729736:role/snowflake-spoify-connection'
STORAGE_ALLOWED_LOCATIONS = ('s3://spotify-etl-project-rakeshs/transformed_data/')
COMMENT = 'Creating connection to s3';


desc integration spotify_init;



CREATE OR REPLACE FILE FORMAT spotify.PUBLIC.CSV_FILE_FORMAT
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1;




CREATE OR REPLACE STAGE spotify.PUBLIC.CSV_FOLDER
URL = 's3://spotify-etl-project-rakeshs/transformed_data/'
STORAGE_INTEGRATION = spotify_init
FILE_FORMAT = spotify.PUBLIC.CSV_FILE_FORMAT;

LIST @spotify.PUBLIC.CSV_FOLDER;




CREATE OR REPLACE PIPE SPOTIFY.PUBLIC.ALBUM_PIPE
auto_ingest = True
as 
copy into spotify.PUBLIC.album_data
from @spotify.PUBLIC.CSV_FOLDER/album_data/;

DESC PIPE SPOTIFY.PUBLIC.ALBUM_PIPE;



CREATE OR REPLACE PIPE SPOTIFY.PUBLIC.ARTIST_PIPE
auto_ingest = True
as 
copy into spotify.PUBLIC.artist_data
from @spotify.PUBLIC.CSV_FOLDER/artist_data/;

DESC PIPE SPOTIFY.PUBLIC.ARTIST_PIPE;



CREATE OR REPLACE PIPE SPOTIFY.PUBLIC.SONGS_PIPE
auto_ingest = True
as 
copy into spotify.PUBLIC.SONGS_data
from @spotify.PUBLIC.CSV_FOLDER/songs_data/;


DESC pipe  SPOTIFY.PUBLIC.SONGS_PIPE;