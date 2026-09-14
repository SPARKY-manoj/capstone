import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3


def run_usecase2():
    conn=sqlite3.connect("chicago_crime.db")
    df=pd.read_sql_query("SELECT * FROM chicago_crime",conn)
    conn.close()

    months=["","January","February","March","April","May","June","July","August","September","October","November","December"]
    monthly_crimes=df["MONTH"].value_counts()
    highest_month=monthly_crimes.idxmax()
    highest_month_count=monthly_crimes.max()
    highest_month_name=months[int(highest_month)]

    yearly_crimes=df.groupby("YEAR").size()

    plt.figure(figsize=(8,4))
    plt.plot(yearly_crimes.index,yearly_crimes.values,marker="o")

    for x,y in zip(yearly_crimes.index,yearly_crimes.values):
        plt.text(x,y+3,str(y),ha="center",va="bottom")

    plt.title("Crime trend over years")
    plt.xlabel("year")
    plt.ylabel("number of crimes")
    plt.margins(y=0.15)
    plt.tight_layout()
    plt.savefig("static/images/crime_trend.png",bbox_inches="tight")
    plt.close()

    top_10_crimes=df["PRIMARY_TYPE"].value_counts().head(10)
    top_10_percent=(top_10_crimes/len(df))*100

    top_10_data=[]

    for crime in top_10_crimes.index:
        top_10_data.append({"crime_type":crime,"count":int(top_10_crimes[crime]),"percentage":round(float(top_10_percent[crime]),2)})

    fig,ax=plt.subplots(figsize=(10,4))
    sns.barplot(x=top_10_crimes.values,y=top_10_crimes.index,ax=ax,color="blue",legend=False)

    for c in ax.containers:
        ax.bar_label(c,padding=3)

    plt.title("top 10 crime category")
    plt.xlabel("count")
    plt.ylabel("crime type")
    plt.tight_layout()
    plt.savefig("static/images/top10_crimes.png",bbox_inches="tight")
    plt.close()

    arrest_rate=df["ARREST"].mean()*100
    yearly_arrest=df.groupby("YEAR")["ARREST"].mean()*100
    yearly_arrest_data=[]

    for year,rate in yearly_arrest.items():
        yearly_arrest_data.append({"year":int(year),"arrest_rate":round(float(rate),2)})

    arrest_rate_min=yearly_arrest.min()
    arrest_rate_max=yearly_arrest.max()
    arrest_rate_difference=arrest_rate_max-arrest_rate_min

    pt=df.pivot_table(index="DAYOFWEEK",columns="MONTH",values="CASE_NUMBER",aggfunc="count").reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    plt.figure(figsize=(10,4))
    sns.heatmap(pt,cmap="YlOrRd",annot=True,fmt=".0f")
    plt.title("crime by month and day of week")
    plt.xlabel("month")
    plt.ylabel("day of week")
    plt.tight_layout()
    plt.savefig("static/images/month_day_heatmap.png",bbox_inches="tight")
    plt.close()

    top_comm=df.loc[df["COMMUNITY_CODE"]!=-1,"COMMUNITY_CODE"].value_counts().head(10)
    top_community_data=[]
    for community,count in top_comm.items():
        top_community_data.append({"community_code":int(community),"crime_count":int(count)})

    fig,ax=plt.subplots(figsize=(10,4))
    sns.barplot(x=top_comm.index.astype(int).astype(str),y=top_comm.values,ax=ax,color="blue",legend=False)

    for c in ax.containers:
        ax.bar_label(c,padding=3)

    plt.title("top 10 community areas with highest crime counts")
    plt.xlabel("community code")
    plt.ylabel("crime count")
    plt.tight_layout()
    plt.margins(y=0.15)
    plt.savefig("static/images/top_communities.png",bbox_inches="tight")
    plt.close()

    most_frequent_crime=top_10_crimes.index[0]
    most_frequent_count=top_10_crimes.iloc[0]
    most_frequent_percentage=top_10_percent.iloc[0]

    yearly_crime_data=[]

    for year,count in yearly_crimes.items():
        yearly_crime_data.append({
            "year":int(year),
            "crime_count":int(count)
        })

    
    results={
        "highest_month":int(highest_month),
        "highest_month_name":highest_month_name,
        "highest_month_count":int(highest_month_count),

        "yearly_crimes":yearly_crime_data,

        "top_10_crimes":top_10_data,

        "most_frequent_crime":most_frequent_crime,
        "most_frequent_count":int(most_frequent_count),
        "most_frequent_percentage":round(float(most_frequent_percentage),2),

        "arrest_rate":round(float(arrest_rate),2),
        "yearly_arrest_rate":yearly_arrest_data,
        "arrest_rate_min":round(float(arrest_rate_min),2),
        "arrest_rate_max":round(float(arrest_rate_max),2),
        "arrest_rate_difference":round(float(arrest_rate_difference),2),

        "top_communities":top_community_data,

        "crime_trend_plot":"static/images/crime_trend.png",
        "top10_crimes_plot":"static/images/top10_crimes.png",
        "month_day_heatmap":"static/images/month_day_heatmap.png",
        "top_communities_plot":"static/images/top_communities.png",

        "status":"Use Case 2 completed successfully"
    }

    return results


if __name__=="__main__":
    result=run_usecase2()

    
