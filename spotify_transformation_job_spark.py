
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
from pyspark.sql.functions import explode, col, to_date
from datetime import datetime
from awsglue.dynamicframe import DynamicFrame
s3_path = "s3://spotify-etl-spark-project-rakesh/raw_data/to_processed/"
source_dyf = glueContext.create_dynamic_frame_from_options(
    connection_type = 's3',
    connection_options = {"paths" :[s3_path]},
    format = "json"
)
spotify_df = source_dyf.toDF()
df = spotify_df
def process_albums(df):
    df = (
        df.withColumn("items", explode("items"))
          .select(
              col("items.track.album.id").alias("album_id"),
              col("items.track.album.name").alias("album_name"),
              col("items.track.album.release_date").alias("release_date"),
              col("items.track.album.total_tracks").alias("total_tracks"),
              col("items.track.album.external_urls.spotify").alias("external_url")
          )
          .dropDuplicates(["album_id"])
    )
    return df


def process_artists(df):
    df_artist_exploded = (
        df.select(explode(col("items")).alias("item"))
          .select(explode(col("item.track.artists")).alias("artist"))
    )

    df_artists = (
        df_artist_exploded.select(
            col("artist.id").alias("artist_id"),
            col("artist.name").alias("artist_name"),
            col("artist.external_urls.spotify").alias("external_url")
        )
        .dropDuplicates(["artist_id"])
    )

    return df_artists


def process_songs(df):
    df_explode = df.select(explode(col("items")).alias("item"))

    df_songs = (
        df_explode.select(
            col("item.track.id").alias("song_id"),
            col("item.track.name").alias("song_name"),
            col("item.track.duration_ms").alias("duration_ms"),
            col("item.track.external_urls.spotify").alias("external_url"),
            col("item.track.popularity").alias("popularity"),
            col("item.added_at").alias("song_added"),
            col("item.track.album.id").alias("album_id"),
            col("item.track.artists")[0]["id"].alias("artist_id")
        )
        .dropDuplicates(["song_id"])
    )

    df_songs = df_songs.withColumn(
        "song_added", to_date(col("song_added"))
    )

    return df_songs

album_df = process_albums(spotify_df)
album_df.show(5)
artist_df = process_artists(spotify_df)
artist_df.show(5)
song_df = process_songs(spotify_df)
song_df.show(5)
def write_to_s3(df, path_suffix, format_type="csv"):
    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

    glueContext.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        connection_options={
            "path": f"s3://spotify-etl-spark-project-rakesh/transformed_data/{path_suffix}/"
        },
        format=format_type
    )

write_to_s3(album_df,"album_data/album_transformed_{}".format(datetime.now().strftime("%y-%m-%d")),"csv")
write_to_s3(artist_df,"artist_data/artist_transformed_{}".format(datetime.now().strftime("%y-%m-%d")),"csv")
write_to_s3(song_df,"songs_data/songs_transformed_{}".format(datetime.now().strftime("%y-%m-%d")),"csv")
def list_s3_objects(bucket, prefix):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket = bucket, Prefix=prefix)
    keys = [content['Key'] for content in response.get('Contents',[]) if content['Key'].endswith('.json')]
    return keys


bucket_name = "spotify-etl-spark-project-rakesh"
prefix = "raw_data/to_processed/"
spotify_keys = list_s3_objects(bucket_name, prefix)

def move_and_delete_files(spotify_keys, Bucket):
    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source = {
            'Bucket' : Bucket,
            'Key': key
        }
        
        destination_key = 'raw_data/processed/' + key.split("/")[-1]
        
        s3_resource.meta.client.copy(copy_source, Bucket, destination_key)
        
        s3_resource.Object(Bucket, key).delete()
        
move_and_delete_files(spotify_keys, bucket_name)
job.commit()