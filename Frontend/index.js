document.querySelector("#submit-btn").addEventListener("click", async function() {
  var statementt = document.querySelector("#statement").value;
    document.querySelector("#resultStatement").innerHTML = statementt;
   await fetch('http://backend:8000/predict', {
    method: 'POST',
    headers: {'content-type':'application/json'},
    body: JSON.stringify({
      input_text: statementt,
    })
  }).then(function(response){
    console.log(response.json);
  }).then(function (data) {
	console.log(data);
}).catch(function(err){
  })

});
