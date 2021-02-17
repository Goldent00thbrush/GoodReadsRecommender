var flag = 0;
var monthly_endpoint= "http://127.0.0.1:3000/monthly_run"

async function postData(url = '', data = {}) { //post the actual data to api 
    // const response = await 

    fetch(url, {

      method: 'POST', 

      headers: {'Content-Type': 'text/plain'}, // to allow it to be sent as POST request not OPTIONS request 

      redirect: 'follow', 

      body: JSON.stringify(data) // body data type must match "Content-Type" header

    }).then(result =>{
      if(flag==1){
        flag = 0;
        document.getElementById('text').innerHTML=result.status;
        document.getElementById('load').style.visibility="hidden";
        document.getElementById('email').value= "";
        document.getElementById('account').value= "";
      }

    }).catch(error =>{
        document.getElementById('text').innerHTML=error;
        document.getElementById('load').style.visibility="hidden";
    })
}

document.getElementById("success").addEventListener("click", function() {
  var email = document.getElementById('email').value;
  var account = document.getElementById('account').value;
  var endpoint= "http://127.0.0.1:3000/add_new"
  if (email != "" || account!= ""){
    flag = 1;
  document.getElementById('load').style.visibility="visible";
  var options= {"email":email, "account":account};
  postData(endpoint, options);
  }
})


function monthly_call(cb) {
  (function loop() {
      var now = new Date();
      if (now.getDate() === 1 && now.getHours() === 0 && now.getMinutes() === 0) {
          cb(monthly_endpoint, {});
      }
      now = new Date();                  // allow for time passing
      var delay = 60000*30 - (now % 60000*30); // exact ms to next minute interval
      setTimeout(loop, delay);
  })();
}
monthly_call(postData);