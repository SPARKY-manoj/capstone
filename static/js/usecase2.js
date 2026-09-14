fetch("/api/usecase2")
.then(response=>response.json())
.then(data=>{
    document.getElementById("mostFrequentCrime").innerText=data.most_frequent_crime;
    document.getElementById("mostFrequentDetails").innerText=data.most_frequent_count+" crimes ("+data.most_frequent_percentage+"%)";

    document.getElementById("arrestRate").innerText=data.arrest_rate+"%";
  

    document.getElementById("highestMonth").innerText=data.highest_month_name;
    document.getElementById("highestMonthCount").innerText=data.highest_month_count+" crimes";

    
  

    let yearlyCrimeTable=document.getElementById("yearlyCrimeTable");
    data.yearly_crimes.forEach(row=>{
        yearlyCrimeTable.innerHTML+=`
        <tr>
            <td>${row.year}</td>
            <td>${row.crime_count}</td>
        </tr>`;
    });

    let top10Table=document.getElementById("top10Table");
    data.top_10_crimes.forEach(row=>{
        top10Table.innerHTML+=`
        <tr>
            <td>${row.crime_type}</td>
            <td>${row.count}</td>
            <td>${row.percentage}%</td>
        </tr>`;
    });

    let yearlyArrestTable=document.getElementById("yearlyArrestTable");
    data.yearly_arrest_rate.forEach(row=>{
        yearlyArrestTable.innerHTML+=`
        <tr>
            <td>${row.year}</td>
            <td>${row.arrest_rate}%</td>
        </tr>`;
    });

    let communityTable=document.getElementById("communityTable");
    data.top_communities.forEach(row=>{
        communityTable.innerHTML+=`
        <tr>
            <td>${row.community_code}</td>
            <td>${row.crime_count}</td>
        </tr>`;
    });

    document.getElementById("questionCrime").innerText=
        data.most_frequent_crime+" with "+data.most_frequent_count+" crimes ("+data.most_frequent_percentage+"%).";

  

    document.getElementById("questionMonth").innerText=
        data.highest_month_name+" with "+data.highest_month_count+" crimes.";
})
.catch(error=>{
    console.log("Error loading Use Case 2:",error);
});