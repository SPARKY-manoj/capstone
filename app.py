from flask import Flask,jsonify,request,send_from_directory
import sqlite3

from use_case_1 import run_usecase1
from use_case_2 import run_usecase2
from use_case_3 import run_usecase3
from use_case_4 import run_usecase4

app=Flask(__name__,static_folder="static")

usecase1_result=run_usecase1()
usecase2_result=run_usecase2()
usecase3_result=run_usecase3()
usecase4_result=run_usecase4()

def get_connection():
    conn=sqlite3.connect("chicago_crime.db")
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/")
def home():
    return send_from_directory("frontend","dashboard.html")

@app.route("/usecase1")
def usecase1_page():
    return send_from_directory("frontend","usecase1.html")

@app.route("/usecase2")
def usecase2_page():
    return send_from_directory("frontend","usecase2.html")

@app.route("/usecase3")
def usecase3_page():
    return send_from_directory("frontend","usecase3.html")

@app.route("/usecase4")
def usecase4_page():
    return send_from_directory("frontend","usecase4.html")

@app.route("/crud")
def crud_page():
    return send_from_directory("frontend","crud.html")

@app.route("/api/dashboard",methods=["GET"])
def dashboard():
    conn=get_connection()

    total_crimes=conn.execute(
        "SELECT COUNT(*) AS total FROM chicago_crime"
    ).fetchone()["total"]

    total_arrests=conn.execute(
        "SELECT COUNT(*) AS total FROM chicago_crime WHERE ARREST=1"
    ).fetchone()["total"]

    conn.close()

    data={
        "total_crimes":total_crimes,
        "total_arrests":total_arrests,
        "arrest_rate":usecase2_result["arrest_rate"],
        "unique_crime_types":usecase1_result["unique_crime_count"],
        "most_frequent_crime":usecase2_result["most_frequent_crime"],
        "most_frequent_count":usecase2_result["most_frequent_count"],
        "highest_crime_month":usecase2_result["highest_month_name"],
        "highest_month_count":usecase2_result["highest_month_count"],
        "peak_crime_hour":usecase3_result["peak_hour"],
        "peak_hour_count":usecase3_result["peak_hour_count"],
        "mean_crime_per_area":usecase3_result["mean_crime_per_area"],
        "minimum_year":usecase1_result["minimum_year"],
        "maximum_year":usecase1_result["maximum_year"],
        "yearly_data":usecase4_result["yearly_data"],
        "top5_crimes":usecase4_result["top5_crimes"]
    }

    return jsonify(data)

@app.route("/api/usecase1",methods=["GET"])
def usecase1():
    return jsonify(usecase1_result)

@app.route("/api/usecase2",methods=["GET"])
def usecase2():
    return jsonify(usecase2_result)

@app.route("/api/usecase3",methods=["GET"])
def usecase3():
    return jsonify(usecase3_result)

@app.route("/api/usecase4",methods=["GET"])
def usecase4():
    return jsonify(usecase4_result)

@app.route("/api/crimes",methods=["GET"])
def get_crimes():
    conn=get_connection()
    crimes=conn.execute("SELECT * FROM chicago_crime ORDER BY ID LIMIT 20").fetchall()
    conn.close()
    return jsonify([dict(row) for row in crimes])

@app.route("/api/crimes/<int:crime_id>",methods=["GET"])
def get_crime(crime_id):
    conn=get_connection()
    crime=conn.execute("SELECT * FROM chicago_crime WHERE ID=?",(crime_id,)).fetchone()
    conn.close()
    if crime is None:
        return jsonify({"message":"Crime record not found"}),404
    return jsonify(dict(crime))

@app.route("/api/crimes",methods=["POST"])
def add_crime():
    data=request.get_json()
    conn=get_connection()
    conn.execute("""
    INSERT INTO chicago_crime
    (ID,CASE_NUMBER,DATE,BLOCK,IUCR_CODE,PRIMARY_TYPE,DESCRIPTION,
    LOCATION_DESC,ARREST,DOMESTIC,BEAT_NUM,DISTRICT_CODE,WARD_NO,
    COMMUNITY_CODE,FBI_CODE,YEAR,MONTH,DAYOFWEEK)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,(
        data["ID"],
        data["CASE_NUMBER"],
        data["DATE"],
        data["BLOCK"],
        data["IUCR_CODE"],
        data["PRIMARY_TYPE"],
        data["DESCRIPTION"],
        data["LOCATION_DESC"],
        data["ARREST"],
        data["DOMESTIC"],
        data["BEAT_NUM"],
        data["DISTRICT_CODE"],
        data["WARD_NO"],
        data["COMMUNITY_CODE"],
        data["FBI_CODE"],
        data["YEAR"],
        data["MONTH"],
        data["DAYOFWEEK"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message":"Crime record added successfully"}),201

@app.route("/api/crimes/<int:crime_id>",methods=["PUT"])
def update_crime(crime_id):
    data=request.get_json()
    conn=get_connection()
    crime=conn.execute("SELECT * FROM chicago_crime WHERE ID=?",(crime_id,)).fetchone()
    if crime is None:
        conn.close()
        return jsonify({"message":"Crime record not found"}),404
    conn.execute("""
    UPDATE chicago_crime
    SET CASE_NUMBER=?,DATE=?,BLOCK=?,IUCR_CODE=?,PRIMARY_TYPE=?,
    DESCRIPTION=?,LOCATION_DESC=?,ARREST=?,DOMESTIC=?,BEAT_NUM=?,
    DISTRICT_CODE=?,WARD_NO=?,COMMUNITY_CODE=?,FBI_CODE=?,YEAR=?,
    MONTH=?,DAYOFWEEK=?
    WHERE ID=?
    """,(
        data["CASE_NUMBER"],
        data["DATE"],
        data["BLOCK"],
        data["IUCR_CODE"],
        data["PRIMARY_TYPE"],
        data["DESCRIPTION"],
        data["LOCATION_DESC"],
        data["ARREST"],
        data["DOMESTIC"],
        data["BEAT_NUM"],
        data["DISTRICT_CODE"],
        data["WARD_NO"],
        data["COMMUNITY_CODE"],
        data["FBI_CODE"],
        data["YEAR"],
        data["MONTH"],
        data["DAYOFWEEK"],
        crime_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message":"Crime record updated successfully"})

@app.route("/api/crimes/<int:crime_id>",methods=["DELETE"])
def delete_crime(crime_id):
    conn=get_connection()
    crime=conn.execute("SELECT * FROM chicago_crime WHERE ID=?",(crime_id,)).fetchone()
    if crime is None:
        conn.close()
        return jsonify({"message":"Crime record not found"}),404
    conn.execute("DELETE FROM chicago_crime WHERE ID=?",(crime_id,))
    conn.commit()
    conn.close()

    return jsonify({"message":"Crime record deleted successfully"})

if __name__=="__main__":
    app.run(debug=False,use_reloader=False)
