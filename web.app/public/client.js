
const btnLogging = document.getElementById('btn_logging');
const pLog = document.getElementById('log');
btnLogging.addEventListener('click', 
    function(e) {
	    
	  pLog.innerHTML = "...";

	  var request = new XMLHttpRequest();
	  request.open('POST', "/logging_on");
	  request.responseType = 'text';
	  request.onload = function() {
	       pLog.innerHTML = request.response;
	  };
	  request.send();
    }
);
