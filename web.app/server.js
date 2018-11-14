#!/usr/bin/env node

const express = require('express');
const app = express();
const { exec } = require('child_process');

logging_on = false;

// serve files from the public directory
app.use(express.static(process.cwd() + '/public'));

// start the express web server listening on 3000
app.listen(3000, () => {
  console.log('listening on 3000');
});

// serve the homepage
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/logging_on', (req, res) => {
    if (!logging_on)
    {
	exec('systemctl start arc_logging.service', 
	(err, stdout, stderr) => {
	    if (err) {
		// node couldn't execute the command
		res.send("ERROR: " + err);
		return;
	    }

	     console.log('stdout: ${stdout}');
	     console.log('stderr: ${stderr}');
	     res.send("Logging ON");
	     logging_on = true;
	});
    } else 
	exec('systemctl stop arc_logging.service', 
	(err, stdout, stderr) => {
	    if (err) {
		// node couldn't execute the command
		res.send("ERROR: " + err);
		return;
	    }

	     console.log('stdout: ${stdout}');
	     console.log('stderr: ${stderr}');
	     res.send("Logging OFF");
	     logging_on = false;
	});

    }
);
