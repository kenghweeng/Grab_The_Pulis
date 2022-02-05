import pandas as pd

def preprocess(df):
    # Filter out invalid accuracy
    df = df[df.accuracy > 0]

    # Filter out negative speed
    df = df[df.speed >= 0]

    # Filter out invalid bearing (android)
    df = df.drop(df[(df.bearing <= 0) & (df.osname == "android")].index)

    # Filter out invalid bearing (ios)
    ## Remove consecutive rows with bearing 180 and take average of the speed of these rows
    df.sort_values(["trj_id", "pingtimestamp"], inplace=True)

    df = df.groupby(((df["bearing"] != df["bearing"].shift()) | (df["bearing"] != 180)).cumsum()).agg({'trj_id':'first','driving_mode':'first','osname':'first', 'pingtimestamp':'first', 'rawlat':'first', 'rawlng':'first', 'speed': lambda x: sum(x)/len(x), 'bearing':'first', 'accuracy':'first', 'time':'first', 'day_of_week':'first', 'month':'first', 'year':'first'})

    df.reset_index(drop=True, inplace=True)

    # Convert Unix Time to TimeStamp
    dt = df["pingtimestamp"].apply(datetime.fromtimestamp)
    
    # Add new Day column to dataframe
    df.insert(10,"day", dt.apply(lambda x: x.day))
    df["day"] = df["day"].astype("uint16")

    # Shift Day of Week to last column
    df.insert(len(df.columns)-1, "day_of_week", df.pop("day_of_week"))

    return df
