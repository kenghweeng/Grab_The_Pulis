import pandas as pd
import datetime as dt

jkt_df = pd.read_feather('data/processed_jkt.ftr')
jkt_df["time"] = pd.to_datetime(jkt_df['pingtimestamp'], unit='s') # defaults goes to GMT+8
jkt_df["time"] = jkt_df["time"].dt.tz_localize('Etc/GMT+7').dt.tz_convert('utc')

jkt_df.reset_index(drop=True).to_feather('data/processed_jkt.ftr')