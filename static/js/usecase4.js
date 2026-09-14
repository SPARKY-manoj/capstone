fetch("/api/usecase4")
.then(response=>response.json())
.then(data=>{
    let summaryTables=document.getElementById("summaryTables");
    summaryTables.innerHTML+=`<li>${data.summary_yearly_table}</li>`;
    summaryTables.innerHTML+=`<li>${data.summary_category_table}</li>`;

    let viewsList=document.getElementById("viewsList");
    data.views.forEach(view=>{
        viewsList.innerHTML+=`<li>${view}</li>`;
    });

    let yearlyTable=document.getElementById("yearlyTable");
    data.yearly_data.forEach(row=>{
        yearlyTable.innerHTML+=`
        <tr>
            <td>${row.year}</td>
            <td>${row.total_crimes}</td>
            <td>${row.total_arrest}</td>
        </tr>`;
    });

    let crimeCountTable=document.getElementById("crimeCountTable");
    data.crime_count_per_year.forEach(row=>{
        crimeCountTable.innerHTML+=`
        <tr>
            <td>${row.year}</td>
            <td>${row.total_crimes}</td>
        </tr>`;
    });

    let arrestCountTable=document.getElementById("arrestCountTable");
    data.arrest_count_per_year.forEach(row=>{
        arrestCountTable.innerHTML+=`
        <tr>
            <td>${row.year}</td>
            <td>${row.total_arrest}</td>
        </tr>`;
    });

    let top5Table=document.getElementById("top5Table");
    data.top5_crimes.forEach(row=>{
        top5Table.innerHTML+=`
        <tr>
            <td>${row.primary_type}</td>
            <td>${row.crime_count}</td>
            <td>${row.percentage}%</td>
        </tr>`;
    });

    document.getElementById("yearlyView").innerText=data.yearly_view;
    document.getElementById("categoryView").innerText=data.category_view;
   
})
.catch(error=>{
    console.log("Error loading Use Case 4:",error);
});