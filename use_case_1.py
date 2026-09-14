import pandas as pd
import numpy as np
import sqlite3

def run_usecase1():
    df=pd.read_csv("Chicago_Datasets_Python/chicago_crime_dataset.csv")

    first_10=df.head(10)
    original_rows=df.shape[0]
    original_columns=df.shape[1]
    schema=df.dtypes.astype(str)

    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    invalid_dates=df["date"].isna().sum()

    duplicate_rows=df.duplicated().sum()
    df.drop_duplicates(inplace=True)

    mis_data=np.mean(df.isnull().values,axis=0)*100
    missing_percentage={}
    columns_above_50=[]

    for column,percentage in zip(df.columns,mis_data):
        missing_percentage[column]=round(float(percentage),2)
        if percentage>50:
            columns_above_50.append(column)

    if len(columns_above_50)>0:
        df.drop(columns=columns_above_50,inplace=True)

    unique_crime_types=df["primary_type"].unique().tolist()
    unique_crime_count=df["primary_type"].nunique()

    df["location_desc"]=df["location_desc"].fillna("unknown")
    df["location"]=df["location"].fillna("unknown")
    df["ward_no"]=df["ward_no"].fillna(-1)
    df["community_code"]=df["community_code"].fillna(-1)
    df["latitude"]=df["latitude"].fillna(0)
    df["longitude"]=df["longitude"].fillna(0)
    df["x_coordinate"]=df["x_coordinate"].fillna(0)
    df["y_coordinate"]=df["y_coordinate"].fillna(0)

    df["year"]=df["date"].dt.year
    df["month"]=df["date"].dt.month
    df["dayofweek"]=df["date"].dt.day_name()

    minimum_year=df["year"].min()
    maximum_year=df["year"].max()

    invalid_years=df[~df["year"].between(2015,2023)]
    invalid_year_count=len(invalid_years)

    df.columns=df.columns.str.upper().str.strip()

    final_rows=df.shape[0]
    final_columns=df.shape[1]

    conn=sqlite3.connect("chicago_crime.db")
    df.to_sql("chicago_crime",conn,if_exists="replace",index=False)
    conn.close()

    results={
        "original_rows":int(original_rows),
        "original_columns":int(original_columns),
        "final_rows":int(final_rows),
        "final_columns":int(final_columns),
        "duplicate_rows":int(duplicate_rows),
        "invalid_dates":int(invalid_dates),
        "unique_crime_count":int(unique_crime_count),
        "unique_crime_types":unique_crime_types,
        "minimum_year":int(minimum_year),
        "maximum_year":int(maximum_year),
        "invalid_year_count":int(invalid_year_count),
        "columns_above_50":columns_above_50,
        "missing_percentage":missing_percentage,
        "schema":schema.to_dict(),
        "first_10_rows":first_10.fillna("").to_dict(orient="records"),
        "database":"chicago_crime.db",
        "table":"chicago_crime",
        "status":"Use Case 1 completed successfully"
    }

    return results


if __name__=="__main__":
    result=run_usecase1()

