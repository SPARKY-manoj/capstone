let editMode=false;
let editId=null;

function loadCrimes(){
    fetch("/api/crimes")
    .then(response=>response.json())
    .then(data=>{
        let table=document.getElementById("crimeTable");
        table.innerHTML="";

        data.forEach(row=>{
            table.innerHTML+=`
            <tr>
                <td>${row.ID}</td>
                <td>${row.CASE_NUMBER}</td>
                <td>${row.DATE}</td>
                <td>${row.PRIMARY_TYPE}</td>
                <td>${row.LOCATION_DESC}</td>
                <td>${row.ARREST==1?"Yes":"No"}</td>
                <td>${row.COMMUNITY_CODE}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editCrime(${row.ID})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCrime(${row.ID})">Delete</button>
                </td>
            </tr>`;
        });
    })
    .catch(error=>console.log("Error loading crimes:",error));
}

document.getElementById("crimeForm").addEventListener("submit",function(event){
    event.preventDefault();

    let data={
        ID:parseInt(document.getElementById("id").value),
        CASE_NUMBER:document.getElementById("caseNumber").value,
        DATE:document.getElementById("date").value.replace("T"," "),
        BLOCK:document.getElementById("block").value,
        IUCR_CODE:parseInt(document.getElementById("iucrCode").value),
        PRIMARY_TYPE:document.getElementById("primaryType").value.toUpperCase(),
        DESCRIPTION:document.getElementById("description").value.toUpperCase(),
        LOCATION_DESC:document.getElementById("locationDesc").value.toUpperCase(),
        ARREST:parseInt(document.getElementById("arrest").value),
        DOMESTIC:parseInt(document.getElementById("domestic").value),
        BEAT_NUM:parseInt(document.getElementById("beatNum").value),
        DISTRICT_CODE:parseInt(document.getElementById("districtCode").value),
        WARD_NO:parseInt(document.getElementById("wardNo").value),
        COMMUNITY_CODE:parseInt(document.getElementById("communityCode").value),
        FBI_CODE:document.getElementById("fbiCode").value.toUpperCase(),
        YEAR:parseInt(document.getElementById("year").value),
        MONTH:parseInt(document.getElementById("month").value),
        DAYOFWEEK:document.getElementById("dayofweek").value
    };

    let url="/api/crimes";
    let method="POST";

    if(editMode){
        url="/api/crimes/"+editId;
        method="PUT";
    }

    fetch(url,{
        method:method,
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    })
    .then(response=>response.json())
    .then(result=>{
        showMessage(result.message);
        resetForm();
        loadCrimes();
    })
    .catch(error=>console.log("Error saving crime:",error));
});

function editCrime(id){
    fetch("/api/crimes/"+id)
    .then(response=>response.json())
    .then(data=>{
        editMode=true;
        editId=id;

        document.getElementById("id").value=data.ID;
        document.getElementById("id").disabled=true;
        document.getElementById("caseNumber").value=data.CASE_NUMBER;

        if(data.DATE){
            document.getElementById("date").value=data.DATE.replace(" ","T").substring(0,16);
        }

        document.getElementById("block").value=data.BLOCK;
        document.getElementById("iucrCode").value=data.IUCR_CODE;
        document.getElementById("primaryType").value=data.PRIMARY_TYPE;
        document.getElementById("description").value=data.DESCRIPTION;
        document.getElementById("locationDesc").value=data.LOCATION_DESC;
        document.getElementById("arrest").value=data.ARREST?1:0;
        document.getElementById("domestic").value=data.DOMESTIC?1:0;
        document.getElementById("beatNum").value=data.BEAT_NUM;
        document.getElementById("districtCode").value=data.DISTRICT_CODE;
        document.getElementById("wardNo").value=data.WARD_NO;
        document.getElementById("communityCode").value=data.COMMUNITY_CODE;
        document.getElementById("fbiCode").value=data.FBI_CODE;
        document.getElementById("year").value=data.YEAR;
        document.getElementById("month").value=data.MONTH;
        document.getElementById("dayofweek").value=data.DAYOFWEEK;

        document.getElementById("saveButton").innerText="Update Crime";
        window.scrollTo({top:0,behavior:"smooth"});
    });
}

function deleteCrime(id){
    if(!confirm("Delete this crime record?")){
        return;
    }

    fetch("/api/crimes/"+id,{
        method:"DELETE"
    })
    .then(response=>response.json())
    .then(result=>{
        showMessage(result.message);
        loadCrimes();
    });
}

function resetForm(){
    editMode=false;
    editId=null;
    document.getElementById("crimeForm").reset();
    document.getElementById("id").disabled=false;
    document.getElementById("saveButton").innerText="Add Crime";
}

function showMessage(message){
    document.getElementById("message").innerHTML=`
    <div class="alert alert-success">${message}</div>`;
}

loadCrimes();