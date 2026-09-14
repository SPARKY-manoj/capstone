fetch("/api/usecase1")
.then(response=>response.json())
.then(data=>{
    document.getElementById("originalRows").innerText=data.original_rows;
    document.getElementById("originalColumns").innerText=data.original_columns;
    document.getElementById("uniqueCrimeCount").innerText=data.unique_crime_count;
    document.getElementById("duplicateRows").innerText=data.duplicate_rows;
    document.getElementById("invalidDates").innerText=data.invalid_dates;
    document.getElementById("yearRange").innerText=data.minimum_year+" - "+data.maximum_year;
    document.getElementById("finalDataset").innerText=data.final_rows+" rows, "+data.final_columns+" columns";
 

    if(data.columns_above_50.length===0){
        document.getElementById("columnsAbove50").innerText="No columns have more than 50% missing values.";
    }else{
        document.getElementById("columnsAbove50").innerText=data.columns_above_50.join(", ");
    }

    document.getElementById("crimeTypes").innerText=data.unique_crime_types.join(", ");

    let missingTable=document.getElementById("missingTable");
    Object.entries(data.missing_percentage).forEach(([column,value])=>{
        missingTable.innerHTML+=`
        <tr>
            <td>${column}</td>
            <td>${value}%</td>
        </tr>`;
    });

    let schemaTable=document.getElementById("schemaTable");
    Object.entries(data.schema).forEach(([column,type])=>{
        schemaTable.innerHTML+=`
        <tr>
            <td>${column}</td>
            <td>${type}</td>
        </tr>`;
    });

    let rows=data.first_10_rows;

    if(rows.length>0){
        let columns=Object.keys(rows[0]);
        let previewHead=document.getElementById("previewHead");
        let previewBody=document.getElementById("previewBody");

        let head="<tr>";
        columns.forEach(column=>{
            head+=`<th>${column}</th>`;
        });
        head+="</tr>";
        previewHead.innerHTML=head;

        rows.forEach(row=>{
            let line="<tr>";
            columns.forEach(column=>{
                line+=`<td>${row[column]}</td>`;
            });
            line+="</tr>";
            previewBody.innerHTML+=line;
        });
    }
})
.catch(error=>{
    console.log("Error loading Use Case 1:",error);
});