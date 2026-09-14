fetch("/api/dashboard")
.then(response=>response.json())
.then(data=>{
    document.getElementById("totalCrimes").innerText=data.total_crimes;
    document.getElementById("totalArrests").innerText=data.total_arrests;
    document.getElementById("arrestRate").innerText=data.arrest_rate+"%";
    document.getElementById("uniqueCrimes").innerText=data.unique_crime_types;
    
    document.getElementById("mostFrequentCrime").innerText=data.most_frequent_crime;
    document.getElementById("mostFrequentCrimeCount").innerText=data.most_frequent_count+" crimes";
    
    document.getElementById("highestMonth").innerText=data.highest_crime_month;
    document.getElementById("highestMonthCount").innerText=data.highest_month_count+" crimes";

    document.getElementById("peakHour").innerText=data.peak_crime_hour+":00";
    document.getElementById("peakHourCount").innerText=data.peak_hour_count+" crimes";

    let yearlyTable=document.getElementById("yearlyTable");
    data.yearly_data.forEach(row=>{
	yearlyTable.innerHTML+=`
	<tr>
	    <td>${row.year}</td>
	    <td>${row.total_crimes}</td>
	    <td>${row.total_arrest}</td>
	</tr>
        `;
    });

    let top5Table=document.getElementById("top5Table");
    data.top5_crimes.forEach(row=>{
	top5Table.innerHTML+=`
	<tr>
	    <td>${row.primary_type}</td>
	    <td>${row.crime_count}</td>
	    <td>${row.percentage}</td> 
	</tr>
	`;
    });
})
.catch(error=>{
    console.log("Errror loadinf dashboard:",error);
})