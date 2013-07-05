var express = require('express');
var python = require('python-shell');
var app = express();

app.get('/', function (req, res) {
	var json = JSON.parse(data);
	var id = json.id;
	var sender = json.sender;
	var text = json.text;
	if (text.toLowerCase().indexOf("hey ericbot") > -1) {
		var options = {
			args = [sender]
		}
		python.run('markov_generator.py', options, function (err, results) {

		});
	} else {
		var options = {
			args = [id, text, sender]
		}
		python.run('insert.py', options, function (err, results) {

		});
	}
	res.send('Hello world!');
});

var server = app.listen(4567, '0.0.0.0');
