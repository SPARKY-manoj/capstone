fetch("/api/usecase3")
.then(response=>response.json())
.then(data=>{
    document.getElementById("peakHour").innerText=data.peak_hour+":00";
    document.getElementById("peakHourCount").innerText=data.peak_hour_count+" crimes";
    document.getElementById("meanCrime").innerText=data.mean_crime_per_area;
    document.getElementById("maxCrime").innerText=data.maximum_crime_per_area;
    document.getElementById("minCrime").innerText=data.minimum_crime_per_area;

    document.getElementById("q1").innerText=data.q1;
    document.getElementById("q3").innerText=data.q3;
    document.getElementById("iqr").innerText=data.iqr;
    document.getElementById("lowerBound").innerText=data.lower_bound;
    document.getElementById("upperBound").innerText=data.upper_bound;
    document.getElementById("outlierCount").innerText=data.outlier_count;

    document.getElementById("correlationExplanation").innerText=data.correlation_explanation;
   

    let hourlyTable=document.getElementById("hourlyTable");
    data.hourly_data.forEach(row=>{
        hourlyTable.innerHTML+=`
        <tr>
            <td>${row.hour}:00</td>
            <td>${row.crime_count}</td>
        </tr>`;
    });

    let outlierTable=document.getElementById("outlierTable");

    if(data.outliers.length===0){
        outlierTable.innerHTML=`
        <tr>
            <td colspan="2">No outlier communities found</td>
        </tr>`;
    }else{
        data.outliers.forEach(row=>{
            outlierTable.innerHTML+=`
            <tr>
                <td>${row.community_code}</td>
                <td>${row.crime_count}</td>
            </tr>`;
        });
    }

    let correlation=data.correlation_matrix;
    let columns=Object.keys(correlation);

    let head="<tr><th>Feature</th>";
    columns.forEach(column=>{
        head+=`<th>${column}</th>`;
    });
    head+="</tr>";
    document.getElementById("correlationHead").innerHTML=head;

    let body="";
    columns.forEach(rowName=>{
        body+=`<tr><th>${rowName}</th>`;
        columns.forEach(columnName=>{
            body+=`<td>${correlation[columnName][rowName]}</td>`;
        });
        body+="</tr>";
    });

    document.getElementById("correlationBody").innerHTML=body;
})
.catch(error=>{
    console.log("Error loading Use Case 3:",error);
});