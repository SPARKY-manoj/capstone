import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def run_usecase4():
    conn=sqlite3.connect("chicago_crime.db")
    cursor=conn.cursor()

    cursor.execute("DROP VIEW IF EXISTS VW_CRIME_YEARLY;")
    cursor.execute("""
    CREATE VIEW VW_CRIME_YEARLY AS
    SELECT YEAR,COUNT(*) AS TOTAL_CRIMES,
    SUM(CASE WHEN ARREST=1 OR ARREST='True' THEN 1 ELSE 0 END) AS TOTAL_ARREST
    FROM chicago_crime
    GROUP BY YEAR;
    """)

    cursor.execute("DROP TABLE IF EXISTS SUMMARY_CRIME_YEARLY;")
    cursor.execute("""
    CREATE TABLE SUMMARY_CRIME_YEARLY AS
    SELECT YEAR,COUNT(*) AS TOTAL_CRIMES,
    SUM(CASE WHEN ARREST=1 OR ARREST='True' THEN 1 ELSE 0 END) AS TOTAL_ARREST
    FROM chicago_crime
    GROUP BY YEAR;
    """)

    cursor.execute("DROP VIEW IF EXISTS VW_CRIME_BY_CATEGORY;")
    cursor.execute("""
    CREATE VIEW VW_CRIME_BY_CATEGORY AS
    SELECT PRIMARY_TYPE,COUNT(*) AS CRIME_COUNT,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM chicago_crime),2) AS PERCENTAGE
    FROM chicago_crime
    GROUP BY PRIMARY_TYPE
    ORDER BY CRIME_COUNT DESC;
    """)

    cursor.execute("DROP TABLE IF EXISTS SUMMARY_CRIME_BY_CATEGORY;")
    cursor.execute("""
    CREATE TABLE SUMMARY_CRIME_BY_CATEGORY AS
    SELECT PRIMARY_TYPE,COUNT(*) AS CRIME_COUNT,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM chicago_crime),2) AS PERCENTAGE
    FROM chicago_crime
    GROUP BY PRIMARY_TYPE
    ORDER BY CRIME_COUNT DESC;
    """)

    conn.commit()

    tables=pd.read_sql_query("""
    SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
    """,conn)

    views=pd.read_sql_query("""
    SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;
    """,conn)

    cursor.execute("""
    SELECT YEAR,TOTAL_CRIMES,TOTAL_ARREST FROM VW_CRIME_YEARLY ORDER BY YEAR;
    """)

    yearly_rows=cursor.fetchall()

    yearly_data=[]

    for row in yearly_rows:
        yearly_data.append({"year":int(row[0]),"total_crimes":int(row[1]),"total_arrest":int(row[2])})

    cursor.execute("""
    SELECT PRIMARY_TYPE,CRIME_COUNT,PERCENTAGE
    FROM VW_CRIME_BY_CATEGORY
    ORDER BY CRIME_COUNT DESC
    LIMIT 5;
    """)

    top5_rows=cursor.fetchall()

    top5_data=[]

    for row in top5_rows:
        top5_data.append({"primary_type":row[0],"crime_count":int(row[1]),"percentage":float(row[2])})

    cursor.execute("""
    SELECT YEAR,TOTAL_CRIMES FROM VW_CRIME_YEARLY ORDER BY YEAR;
    """)

    crime_count_per_year=[]

    for row in cursor.fetchall():
        crime_count_per_year.append({"year":int(row[0]),"total_crimes":int(row[1])})

    cursor.execute("""
    SELECT YEAR,TOTAL_ARREST
    FROM VW_CRIME_YEARLY
    ORDER BY YEAR;
    """)

    arrest_count_per_year=[]

    for row in cursor.fetchall():
        arrest_count_per_year.append({"year":int(row[0]),"total_arrest":int(row[1])})

    df_yearly=pd.read_sql_query("SELECT * FROM VW_CRIME_YEARLY ORDER BY YEAR",conn)

    df_categories=pd.read_sql_query("SELECT * FROM VW_CRIME_BY_CATEGORY ORDER BY CRIME_COUNT DESC",conn)

    conn.close()

    plt.figure(figsize=(10,6))
    plt.plot(df_yearly["YEAR"],df_yearly["TOTAL_CRIMES"],marker="o",label="total crimes")

    plt.plot(df_yearly["YEAR"],df_yearly["TOTAL_ARREST"],marker="s",color="green",label="total arrests")

    for x,y in zip(df_yearly["YEAR"],df_yearly["TOTAL_CRIMES"]):
        plt.text(x,y+5,str(y),ha="center",va="bottom")

    for x,y in zip(df_yearly["YEAR"],df_yearly["TOTAL_ARREST"]):
        plt.text(x,y+5,str(y),ha="center",va="bottom")

    plt.title("total crimes VS total arrests")
    plt.xlabel("year")
    plt.ylabel("count")
    plt.margins(y=0.15)
    plt.tight_layout()
    plt.legend()
    plt.savefig("static/images/crimes_vs_arrests.png",bbox_inches="tight")
    plt.close()

    fig,ax=plt.subplots(figsize=(10,6))

    sns.barplot(data=df_categories.head(5),x="PERCENTAGE",y="PRIMARY_TYPE",color="blue",ax=ax,legend=False)

    for c in ax.containers:
        ax.bar_label(c,fmt="%.2f%%",padding=3)

    plt.title("top 5 crime categories")
    plt.xlabel("percentage")
    plt.ylabel("crime category")
    plt.margins(x=0.15)
    plt.tight_layout()
    plt.savefig("static/images/top5_categories.png",bbox_inches="tight")
    plt.close()

    table_names=tables["name"].tolist()
    view_names=views["name"].tolist()

    results={
        "tables":table_names,
        "views":view_names,

        "yearly_data":yearly_data,
        "crime_count_per_year":crime_count_per_year,
        "arrest_count_per_year":arrest_count_per_year,

        "top5_crimes":top5_data,

        "summary_yearly_table":"SUMMARY_CRIME_YEARLY",
        "summary_category_table":"SUMMARY_CRIME_BY_CATEGORY",

        "yearly_view":"VW_CRIME_YEARLY",
        "category_view":"VW_CRIME_BY_CATEGORY",

        "crimes_vs_arrests_plot":"static/images/crimes_vs_arrests.png",
        "top5_categories_plot":"static/images/top5_categories.png",

        "status":"Use Case 4 completed successfully"
    }

    return results


if __name__=="__main__":
    result=run_usecase4()

    
