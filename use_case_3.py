import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def run_usecase3():
    conn=sqlite3.connect("chicago_crime.db")
    df=pd.read_sql_query("SELECT * FROM chicago_crime",conn)
    conn.close()

    df["DATE"]=pd.to_datetime(df["DATE"])
    df["HOUR"]=df["DATE"].dt.hour

    crimes_by_hour=df.groupby("HOUR").size()

    plt.figure(figsize=(10,6))
    plt.plot(crimes_by_hour.index,crimes_by_hour.values,marker="o",color="blue")

    for x,y in zip(crimes_by_hour.index,crimes_by_hour.values):
        plt.text(x,y+5,str(y),ha="center",va="bottom")

    plt.title("crime intensity by the hours of a day")
    plt.xlabel("hour")
    plt.ylabel("number of crimes")
    plt.xticks(range(0,24))
    plt.tight_layout()
    plt.margins(y=0.15)
    plt.savefig("static/images/hourly_crimes.png",bbox_inches="tight")
    plt.close()

    peak_hour=crimes_by_hour.idxmax()
    peak_hour_count=crimes_by_hour.max()

    hourly_data=[]

    for hour,count in crimes_by_hour.items():
        hourly_data.append({"hour":int(hour),"crime_count":int(count)})

    comm=df[df["COMMUNITY_CODE"]!=-1]
    comm_count=comm.groupby("COMMUNITY_CODE").size()

    mean_crime=np.mean(comm_count.values)
    maximum_crime=np.max(comm_count.values)
    minimum_crime=np.min(comm_count.values)

    plt.figure(figsize=(8,4))
    sns.boxplot(x=comm_count.values)
    plt.title("crime distribution")
    plt.xlabel("crime count per area")
    plt.tight_layout()
    plt.savefig("static/images/community_boxplot.png",bbox_inches="tight")
    plt.close()

    q1=np.percentile(comm_count.values,25)
    q3=np.percentile(comm_count.values,75)
    iqr=q3-q1

    lower_bound=q1-(1.5*iqr)
    upper_bound=q3+(1.5*iqr)

    outliers=comm_count[(comm_count<lower_bound) |(comm_count>upper_bound)]

    outlier_data=[]
    for community,count in outliers.items():
        outlier_data.append({"community_code":int(community),"crime_count":int(count)})

    df["ARREST_F"]=df["ARREST"].astype(int)
    df["DOMESTIC_F"]=df["DOMESTIC"].astype(int)

    meaningful_cols=["YEAR","MONTH","HOUR","ARREST_F","DOMESTIC_F","COMMUNITY_CODE"]

    corr_matrix=df[meaningful_cols].corr()

    plt.figure(figsize=(10,6))
    sns.heatmap(corr_matrix,annot=True,fmt=".2f",cmap="coolwarm")
    plt.title("crime cross-correlation")
    plt.tight_layout()
    plt.savefig("static/images/correlation_heatmap.png",bbox_inches="tight")
    plt.close()

    correlation_data=corr_matrix.round(2).to_dict()

    results={
        "peak_hour":int(peak_hour),
        "peak_hour_count":int(peak_hour_count),
        "hourly_data":hourly_data,

        "mean_crime_per_area":round(float(mean_crime),2),
        "maximum_crime_per_area":int(maximum_crime),
        "minimum_crime_per_area":int(minimum_crime),

        "q1":round(float(q1),2),
        "q3":round(float(q3),2),
        "iqr":round(float(iqr),2),
        "lower_bound":round(float(lower_bound),2),
        "upper_bound":round(float(upper_bound),2),

        "outlier_count":len(outliers),
        "outliers":outlier_data,

        "correlation_matrix":correlation_data,
        "correlation_explanation":"Most correlation values are close to 0, so there is no strong linear relationship between the selected features.",

        "hourly_crimes_plot":"static/images/hourly_crimes.png",
        "community_boxplot":"static/images/community_boxplot.png",
        "correlation_heatmap":"static/images/correlation_heatmap.png",

        "status":"Use Case 3 completed successfully"
    }

    return results


if __name__=="__main__":
    result=run_usecase3()
