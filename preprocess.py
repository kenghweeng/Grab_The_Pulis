import pandas as pd
from datetime import datetime

def ios_bearing_check(df):
    df = df.groupby(((df["bearing"] != df["bearing"].shift()) | (df["bearing"] != 180)).cumsum()).agg({'trj_id':'first','driving_mode':'first','pingtimestamp':'first', 'rawlat':'first', 'rawlng':'first', 'speed': lambda x: sum(x)/len(x), 'bearing':'first', 'accuracy':'first'})
    df.reset_index(drop=True, inplace=True)
    return df

def preprocess(df):
    # Filter out invalid accuracy
    df = df[df.accuracy > 0]

    # Limit accuracy <= 1000
    df = df[df.accuracy <= 1000]

    # Filter out negative speed
    df = df[df.speed >= 0]

    # Filter out invalid bearing (android)
    df = df.drop(df[(df.bearing <= 0) & (df.osname == "android")].index)

    # Filter out invalid bearing (ios)
    ## Remove consecutive rows with bearing 180 and take average of the speed of these rows
    df_ios = df[df.osname == "ios"]
    df_android = df[df.osname == "android"]
    
    suspects = list(set(df_ios.loc[df_ios.index[df_ios['bearing'] == 180]].trj_id))
    df_ios_norm = df_ios[~df_ios.trj_id.isin(suspects)]
    df_ios = df_ios[df_ios.trj_id.isin(suspects)]
    df_ios = df_ios.sort_values(["trj_id", "pingtimestamp"])

    all_dfs = [df_ios[df_ios.trj_id == i] for i in suspects]

    # Check individual df
    all_dfs = list(map(lambda x: ios_bearing_check(x), all_dfs))

    # Combine back to ios
    df_ios = pd.concat(all_dfs)

    # Add back columns
    df_ios['osname'] = 'ios'
    dt = df_ios["pingtimestamp"].apply(datetime.fromtimestamp)
    df_ios["time"] = dt.apply(lambda x: x.time())
    df_ios["day_of_week"] = dt.apply(lambda x: x.weekday())
    df_ios["month"] = dt.apply(lambda x: x.month)
    df_ios["year"] = dt.apply(lambda x: x.year)

    # Combine back ios and android
    df = pd.concat([df_ios, df_ios_norm, df_android])
    dt = df["pingtimestamp"].apply(datetime.fromtimestamp)
    
    # Add new Day column to dataframe
    df.insert(10,"day", dt.apply(lambda x: x.day))
    df["day"] = df["day"].astype("uint16")

    # Shift Day of Week to last column
    df.insert(len(df.columns)-1, "day_of_week", df.pop("day_of_week"))

    return df
