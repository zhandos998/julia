const loadingFDM = document.getElementById('FDM-load');
const loadingFDMtext = document.getElementById('FDM-text');

const loadingTable = document.getElementById('Table-load');
// const loadingTabletext = document.getElementById('Table-text');

const loadingVideoU = document.getElementById('Video-load-u');
// const loadingVideotext = document.getElementById('Video-text');

const loadingVideoV = document.getElementById('Video-load-v');
// const loadingVideotext = document.getElementById('Video-text');
const loadingDownloading = document.getElementById('Downloading-load');

const timer_u = document.getElementById("Video-load-u-text");
const timer_v = document.getElementById("Video-load-v-text");
const timer_julia = document.getElementById("julia-text");
const timer_zip = document.getElementById("zip-text");

function timedifferents(start,end){

    // Вычисляем разницу в миллисекундах
    const differenceInMilliseconds = end - start;
    // if (differenceInMilliseconds<0)
    // differenceInMilliseconds = end;
  
    // Преобразуем разницу в секунды, минуты и часы
    const milliseconds = differenceInMilliseconds % 1000;
    const seconds = Math.floor(differenceInMilliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
  
    // Вычисляем остаток секунд и минут после вычисления часов
    const remainingMinutes = minutes % 60;
    const remainingSeconds = seconds % 60;
    
    return {
        hours:hours,
        minutes:remainingMinutes,
        seconds:remainingSeconds,
        milliseconds:milliseconds,
    };
  
}

function createTimer(el,el_name,start = 0, end = 0) {

    let milliseconds = 0;
    let seconds = 0;
    let minutes = 0;
    let hours = 0;
    if (start!=0 && end!=0 && end>start){
        var diffdate = timedifferents(start,end);
        hours = diffdate.hours;
        minutes = diffdate.minutes;
        seconds = diffdate.seconds;
        milliseconds = diffdate.milliseconds;
    }

    let interval;

    const timer = document.createElement('div');
    timer.innerText = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`
    el.appendChild(timer);

    const startButton = document.createElement('button');
    startButton.innerText = 'Старт';
    startButton.style.display = 'none';
    startButton.setAttribute("id", 'startButton-' + el_name);
    el.appendChild(startButton);

    const stopButton = document.createElement('button');
    stopButton.innerText = 'Стоп';
    stopButton.style.display = 'none';
    stopButton.setAttribute("id", 'stopButton-' + el_name);
    el.appendChild(stopButton);

    function updateTimer() {
      milliseconds += 10;
      if (milliseconds === 1000) {
        milliseconds = 0;
        seconds++;
        if (seconds === 60) {
          seconds = 0;
          minutes++;
          if (minutes === 60) {
            minutes = 0;
            hours++;
          }
        }
      }

      timer.innerText = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`;
    }

    startButton.addEventListener('click', function () {
        
      milliseconds = 0;
      seconds = 0;
      minutes = 0;
      hours = 0;
      interval = setInterval(updateTimer, 10);

    });

    stopButton.addEventListener('click', function () {
      clearInterval(interval);

    });

  }


// var start = Date.parse("{{julia_start}}");
// var end = Date.parse("{{julia_finish}}");
// createTimer(timer_u,'timer-u',Date.parse("{{generate_video_u_start}}"),Date.parse("{{generate_video_u_finish}}"));
// createTimer(timer_v,'timer-v',Date.parse("{{generate_video_v_start}}"),Date.parse("{{generate_video_v_finish}}"));
// createTimer(timer_julia,'timer-julia',Date.parse("{{julia_start}}"),Date.parse("{{julia_finish}}"));
// createTimer(timer_zip,'timer-zip',Date.parse("{{download_start}}"),Date.parse("{{download_finish}}"));



function julia_submit() {
    var startTime = new Date();
    document.getElementById("startButton-timer-julia").click();
    document.getElementById("julia-FDM").disabled = true;
    document.getElementById("generate-video-u").disabled = true;
    document.getElementById("generate-video-v").disabled = true;
    document.getElementById("get-dataset-zip").disabled = true;
    document.getElementById("log").innerHTML = '';
    var form_data = new FormData(document.getElementById("form"));
    form_data.append('startTime', startTime);
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
            document.getElementById("julia-FDM").disabled = false;
            document.getElementById("generate-video-u").disabled = false;
            document.getElementById("generate-video-v").disabled = false;
            document.getElementById("get-dataset-zip").disabled = false;
            document.getElementById("stopButton-timer-julia").click();
            
        },
        error:function (){
            alert('error');
            hideLoadingJulia();
            document.getElementById("julia-FDM").disabled = false;
            document.getElementById("generate-video-u").disabled = false;
            document.getElementById("generate-video-v").disabled = false;
            document.getElementById("get-dataset-zip").disabled = false;
            document.getElementById("stopButton-timer-julia").click();
        }
    });
}

// function view_data(){
//     var form_data = new FormData();
//     form_data.append('data_path', document.getElementById("data_path").value);
//     var jsonData;
//     showLoadingTable();
//     $.ajax({
//         type: "POST",
//         url: "/datasets",
//         contentType: false,
//         cache: false,
//         processData: false,
//         enctype: 'multipart/form-data',
//         data: form_data,
//         timeout:0,
//         success: function(response)
//         {
//             jsonData = JSON.parse(response);
            
//             var table = document.getElementById('myTable');
//             var tbody = table.querySelector('tbody');
//             var thead = table.querySelector('thead');
//             tbody.innerHTML = '';
//             thead.innerHTML = '';
            
//             document.getElementById("log").innerHTML = Object.keys(jsonData.x1).length;
//             let col_length = Object.keys(jsonData).length;
//             let row_length = Object.keys(jsonData.x1).length;

            
//             var row = document.createElement('tr');
//             row.innerHTML = `<th scope="col">#</th>`;
//             tbody.appendChild(row);


//             for(let i=0;i<col_length;i++){
//                 row.innerHTML += `<th scope="col">${Object.keys(jsonData)[i]}</th>`;
//             }
//             tbody.appendChild(row);
            
//             for(let j=0;j<row_length;j++){
//                 setTimeout(function() {
//                     row = document.createElement('tr');
//                     row.innerHTML += `<td>${j}</td>`;
//                     for(let i=0;i<col_length;i++){
//                         row.innerHTML +=  `<td>${jsonData[Object.keys(jsonData)[i]][j]}</td>`;
//                     }
//                     tbody.appendChild(row);
//                 }, 1);
//             }
//             hideLoadingTable();

//         },
//         error:function (){
//             alert('error');
//             hideLoadingTable();
//         }
//     });
// }

function generate_video(method) {
    var startTime = new Date();
    document.getElementById("julia-FDM").disabled = true;
    // document.getElementById("get-dataset-zip").disabled = true;
    var form_data = new FormData();
    form_data.append('method', method);
    form_data.append('startTime', startTime);
    if (method=='u')
    {
        document.getElementById("startButton-timer-u").click();
        document.getElementById("Video-load-u-text").querySelector('span').innerHTML = '';
        document.getElementById("generate-video-u").disabled = true;
        document.getElementById("generate-video-v").disabled = true;
        showLoadingVideoU();
    }
    else
    {
        document.getElementById("startButton-timer-v").click();
        document.getElementById("Video-load-v-text").querySelector('span').innerHTML = '';
        document.getElementById("generate-video-u").disabled = true;
        document.getElementById("generate-video-v").disabled = true;
        showLoadingVideoV();
    }
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
            if (method=='u')
            {
                document.getElementById("my-video-u").querySelector('source').src = response;
                let my_video = document.getElementById("my-video-u").querySelector('video');
                my_video.src = response;
    
                my_video.load();

                document.getElementById("generate-video-v").disabled = false;
                document.getElementById("generate-video-u").disabled = false;
                hideLoadingVideoU();

                document.getElementById("stopButton-timer-u").click();
            }
            else
            {
                document.getElementById("my-video-v").querySelector('source').src = response;
                let my_video = document.getElementById("my-video-v").querySelector('video');
                my_video.src = response;
    
                my_video.load();
                
                document.getElementById("generate-video-v").disabled = false;
                document.getElementById("generate-video-u").disabled = false;
                hideLoadingVideoV();
            
                document.getElementById("stopButton-timer-v").click();
            }

            document.getElementById("julia-FDM").disabled = false;
        },
        error:function (){
            alert('error');
            hideLoadingVideoU();
            hideLoadingVideoV();
            document.getElementById("julia-FDM").disabled = false;
            document.getElementById("generate-video-u").disabled = false;
            document.getElementById("stopButton-timer-u").click();
            document.getElementById("stopButton-timer-v").click();
        }
    });
}

function get_dataset() {
            
    document.getElementById("startButton-timer-zip").click();
    var startTime = new Date();
    document.getElementById("julia-FDM").disabled = true;
    document.getElementById("generate-video-u").disabled = true;
    document.getElementById("generate-video-v").disabled = true;
    document.getElementById("get-dataset-zip").disabled = true;
    showLoadingDownloading();
    var form_data = new FormData();
    form_data.append('startTime', startTime);
    $.ajax({
        type: "POST",
        url: "/get_dataset",
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        data: form_data,
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
            const customFormat = `${year}_${month + 1}_${day}_${hour}_${minute}_${second}`;

            downloadFile(response, `data_${customFormat}.zip`);
            document.getElementById("log").innerHTML = response;
            hideLoadingDownloading();
            
            document.getElementById("julia-FDM").disabled = false;
            document.getElementById("generate-video-u").disabled = false;
            document.getElementById("generate-video-v").disabled = false;
            document.getElementById("get-dataset-zip").disabled = false;

            document.getElementById("stopButton-timer-zip").click();
        },
        error:function (){
            alert('error');
            hideLoadingDownloading();
            document.getElementById("julia-FDM").disabled = false;
            document.getElementById("generate-video-u").disabled = false;
            document.getElementById("generate-video-v").disabled = false;
            document.getElementById("get-dataset-zip").disabled = false;
            document.getElementById("stopButton-timer-zip").click();
        }
    });
}

// ---------------------------------------------------------------------------

function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;

    // Simulate a click on the link to trigger the download
    link.click();

    // Clean up the link element
    // document.body.removeChild(link);
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

function secondsToHMS(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
  
    const hoursStr = String(hours).padStart(2, '0');
    const minutesStr = String(minutes).padStart(2, '0');
    const secondsStr = String(remainingSeconds).padStart(2, '0');
  
    return `${hoursStr}:${minutesStr}:${secondsStr}`;
  }