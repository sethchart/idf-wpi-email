from mysql.connector import connect
from datetime import datetime
import pandas as pd
import numpy as np


def query_civi(DBpwd, query):
    cnx = connect(
        user="idf_ro",
        password=DBpwd,
        host="127.0.0.1",
        database="idf_prod_civicrm",
        port=3306,
    )
    cursor = cnx.cursor()
    df = pd.read_sql(query, cnx)
    cursor.close()
    cnx.close()
    return df


def cosd(t):
    cosd = np.cos(t * np.pi / 180)
    return cosd


def sind(t):
    sind = np.sin(t * np.pi / 180)
    return sind


def euclidian_coords(lon, lat):
    # All quantities below are measured in units of earth radii: 3,958.7613 mi
    rho = 1
    z = rho * sind(lat)
    r = rho * cosd(lat)
    x = r * cosd(lon)
    y = r * sind(lon)
    v = [x, y, z]
    return v


def geodesic_dist(u, v):
    # All quantities below are measured in units of earth radii: 3,958.7613 mi
    rho = 1
    gd = rho * np.arccos(np.dot(u, v) / np.sqrt(np.dot(u, u) * np.dot(v, v)))
    return gd


def closer_point(v, w1, w2):
    if geodesic_dist(v, w1) < geodesic_dist(v, w2):
        return True
    else:
        return False


def closest_walk(lonlat, df_w):
    if (-180 < lonlat[0] < 180) and (-90 < lonlat[1] < 90):
        i = 0
        j = 1
        v = euclidian_coords(lonlat[0], lonlat[1])

        while i < len(df_w) and j < len(df_w):
            w1 = euclidian_coords(df_w.lon[i], df_w.lat[i])
            w2 = euclidian_coords(df_w.lon[j], df_w.lat[j])
            if closer_point(v, w1, w2):
                j += 1
            else:
                i = j
                j += 1

        w = euclidian_coords(df_w.lon[i], df_w.lat[i])
        d = geodesic_dist(v, w)
        # Convert from miles to earth radii
        rad_max = df_w.rad[i] / 3958.7613
        if d <= rad_max:
            walk = df_w.city[i]
        else:
            walk = "Virtual"
    else:
        walk = "Geocode Error"

    return walk


def geotagger(df_w, df):
    walk = df.apply(lambda x: closest_walk([x[6], x[7]], df_w), axis=1)
    df["Closest_Walk"] = walk
    df_tag = df
    return df_tag


def main_process(DBpwd):
    df_w = pd.read_csv("config.csv")
    print("Imported walk locations from config.csv.")
    query_file = open("query.sql", "r")
    print("Imported main query from query.sql.")
    event_ids = tuple(df_w.event_id)
    query = query_file.read().format(event_ids)
    query_file.close()
    print("Inserted event IDs from config.csv into main query.")
    df = query_civi(DBpwd, query)
    print("Imported contact list from CiviCRM.")
    df_tag = geotagger(df_w, df)
    print("Geotagged contacts with closest walk.")
    df_tag = df_tag.dropna(
        subset=["Walk_Email_Subscribed", "Event_Registered"], thresh=1
    )
    df_tag = df_tag.dropna(subset=["Email"])
    df_tag = df_tag.drop(["Lon", "Lat"], axis=1)
    today_date = datetime.today()
    today_str = today_date.strftime("%Y-%m-%d")
    output_file_name = "./output/Walk_Email_List-{0}.csv".format(today_str)
    df_tag.to_csv(output_file_name)
    print("Walk email list saved to {}.".format(output_file_name))


DBpwd = input("Database Password:")
main_process(DBpwd)
