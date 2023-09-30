const loadingFDM = document.getElementById('FDM-load');
const loadingFDMtext = document.getElementById('FDM-text');

const loadingTable = document.getElementById('Table-load');
// const loadingTabletext = document.getElementById('Table-text');

const loadingVideoU = document.getElementById('Video-load-u');
// const loadingVideotext = document.getElementById('Video-text');

const loadingVideoV = document.getElementById('Video-load-v');
// const loadingVideotext = document.getElementById('Video-text');
const loadingDownloading = document.getElementById('Downloading-load');


function submit() {
    var form_data = new FormData(document.getElementById("form"));
    console.log(form_data);
    showLoadingJulia();
    $.ajax({
        type: "POST",
        url: "/solve",
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        data: form_data,
        timeout:0,
        success: function(response)
        {
            document.getElementById("log").innerHTML = response;
            hideLoadingJulia();
        },
        error:function (){
            alert('error');
            hideLoadingJulia();
        }
    });
}

function view_data(){
    var form_data = new FormData();
    form_data.append('data_path', document.getElementById("data_path").value);
    var jsonData;
    showLoadingTable();
    $.ajax({
        type: "POST",
        url: "/datasets",
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        data: form_data,
        timeout:0,
        success: function(response)
        {
            jsonData = JSON.parse(response);
            
            var table = document.getElementById('myTable');
            var tbody = table.querySelector('tbody');
            var thead = table.querySelector('thead');
            tbody.innerHTML = '';
            thead.innerHTML = '';
            
            document.getElementById("log").innerHTML = Object.keys(jsonData.x1).length;
            let col_length = Object.keys(jsonData).length;
            let row_length = Object.keys(jsonData.x1).length;

            
            var row = document.createElement('tr');
            row.innerHTML = `<th scope="col">#</th>`;
            tbody.appendChild(row);


            for(let i=0;i<col_length;i++){
                row.innerHTML += `<th scope="col">${Object.keys(jsonData)[i]}</th>`;
            }
            tbody.appendChild(row);
            
            for(let j=0;j<row_length;j++){
                setTimeout(function() {
                    row = document.createElement('tr');
                    row.innerHTML += `<td>${j}</td>`;
                    for(let i=0;i<col_length;i++){
                        row.innerHTML +=  `<td>${jsonData[Object.keys(jsonData)[i]][j]}</td>`;
                    }
                    tbody.appendChild(row);
                }, 1);
            }
            hideLoadingTable();

        },
        error:function (){
            alert('error');
            hideLoadingTable();
        }
    });
}

function generate_video(method) {
    var form_data = new FormData();
    form_data.append('method', method);
    if (method=='u')
        showLoadingVideoU();
    else
        showLoadingVideoV();
    $.ajax({
        type: "POST",
        url: "/generate-video",
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        data: form_data,
        timeout:0,
        success: function(response)
        {
            document.getElementById("my-video").querySelector('source').src = response;
            let my_video = document.getElementById("my-video").querySelector('video');
            my_video.src = response;

            my_video.load();
            hideLoadingVideoU();
            hideLoadingVideoV();
        },
        error:function (){
            alert('error');
            hideLoadingVideoU();
            hideLoadingVideoV();
        }
    });
}

function get_dataset() {
    showLoadingDownloading();
    $.ajax({
        type: "POST",
        url: "/get_dataset",
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        timeout: 0,
        success: function(response)
        {
            const currentDate = new Date();
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth(); // Month is zero-based (0 = January, 11 = December)
            const day = currentDate.getDate();
            const hour = currentDate.getHours();
            const minute = currentDate.getMinutes();
            const second = currentDate.getSeconds();
            const customFormat = `${year}-${month + 1}-${day} ${hour}:${minute}:${second}`;
            downloadFile(response, `data_${customFormat}.zip`);
            document.getElementById("log").innerHTML = response;
            hideLoadingDownloading();
        },
        error:function (){
            alert('error');
            hideLoadingDownloading();
        }
    });
}

function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;

    // Simulate a click on the link to trigger the download
    link.click();

    // Clean up the link element
    document.body.removeChild(link);
}

function showLoadingJulia() {
    loadingFDM.style.display = 'block';
    loadingFDMtext.style.display = 'none';
}

function hideLoadingJulia() {
    loadingFDM.style.display = 'none';
    loadingFDMtext.style.display = 'block';
}

function showLoadingTable() {
    loadingTable.style.display = 'block';
    // loadingTabletext.style.display = 'none';
}

function hideLoadingTable() {
    loadingTable.style.display = 'none';
    // loadingTabletext.style.display = 'block';
}

function showLoadingVideoU() {
    loadingVideoU.style.display = 'block';
    // loadingVideotext.style.display = 'none';
}

function hideLoadingVideoU() {
    loadingVideoU.style.display = 'none';
    // loadingVideotext.style.display = 'block';
}

function showLoadingVideoV() {
    loadingVideoV.style.display = 'block';
    // loadingVideotext.style.display = 'none';
}

function hideLoadingVideoV() {
    loadingVideoV.style.display = 'none';
    // loadingVideotext.style.display = 'block';
}

function showLoadingDownloading() {
    loadingDownloading.style.display = 'block';
    // loadingVideotext.style.display = 'none';
}

function hideLoadingDownloading() {
    loadingDownloading.style.display = 'none';
    // loadingVideotext.style.display = 'block';
}