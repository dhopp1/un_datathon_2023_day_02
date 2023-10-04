import os
import pandas as pd
### if the module is in a different directory
# import sys
# sys.path.append("path/containing/library/folder/")
from datathon.data_collection import currency_convert, get_oecd, get_pink_sheet

# get ais data
ais = pd.read_csv("https://raw.githubusercontent.com/dhopp1/ais_russia_data/main/russian_port_data.csv", parse_dates = ["date"])
ais["date"] = pd.to_datetime([str(x)[:7] + "-01" for x in ais["date"]]) # aggregate to monthly
ais = ais.loc[:, ["date", "geo_name", "num_ships"]].groupby(["date", "geo_name"]).sum().reset_index()

# make geo_names suitable for column names
ais["geo_name"] = ais["geo_name"].str.replace("-", "_").str.replace(" ", "_").str.replace(".", "").str.lower()
ais = ais.pivot_table(index = ["date"], columns = "geo_name", values = "num_ships").reset_index().fillna(0)

# drop small ports
ais = ais.drop(["sevastopol", "taman"], axis = 1)

# get OECD data
end_date = "2023-08"
start_date = "2019-01"
geos = ["RUS"]; geos = "+".join(geos) # in case there are multiple geographies
dataset = "MEI_ARCHIVE"
variables = ["703"]; variables = "+".join(variables)

# API call
url = f"https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/{dataset}/{geos}.{variables}/all?startTime={start_date}&endTime={end_date}"
oecd = get_oecd(url)

# keep 1 value per month, from the latest edition
oecd = oecd.sort_values(["obsTime", "EDI"]).groupby("obsTime").tail(1).reset_index(drop = True)

# convert obsTime to a date
oecd["obsTime"] = pd.to_datetime(oecd["obsTime"] + "-01")

# convert to USD
oecd["exports_usd"] = currency_convert(oecd.loc[:, ["obsTime", "obsValue"]].set_index("obsTime"), "RUB", "USD")

# get World Bank Pink Sheet data
wb = get_pink_sheet(desired_columns = ["crude_brent", "ngas_us", "ngas_eur", "ngas_jp"], desired_tab = "Monthly Prices")

#  combine OECD and ais data
data = oecd.rename({"obsTime": "date"}, axis = 1).loc[:, ["date", "exports_usd"]].merge(ais, on = "date", how = "outer")

# combine wb data
data = data.merge(wb, on = "date", how = "left")

# writing data out
for col in data.columns[1:]:
    data[col] = data[col].astype(float)
if not(os.path.exists("data/")):
    os.mkdir("data/")
data.to_csv("data/data.csv", index = False)