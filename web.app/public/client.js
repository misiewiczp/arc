
const btnLogging = document.getElementById('btn_logging');
btnLogging.addEventListener('click', 
    function(e) {

	  var request = new XMLHttpRequest();
	  request.open('POST', "/logging_on");
	  request.responseType = 'text';
	  request.onload = function() {
	       btnLogging.value = request.response;
	  };
	  request.send();
    }
);
