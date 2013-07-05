var express = require('express');
var parser = require('body-parser');
var python = require('python-shell');
var app = express();

app.set('port', (process.env.PORT || 5000));

app.use(express.static(__dirname + '/public'));
app.use(parser.json());

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.post('/', function(request, response) {
	var json = request.body;
	var id = json.id;
	var sender = json.sender;
	var text = json.text;
	if (text.toLowerCase().indexOf("hey ericbot") > -1) {
		var options = {
			mode: text,
			args: [sender]
		}
		python.run('list.py', options, function (err, results) {
			console.log("error gen: %s", err)
			console.log("results post: %s", results)
			response.send("good");
			// response.send(results);
		});
	} else {
		var options = {
			mode: text,
			args: [id, text, sender]
		}
		python.run('list.py', options, function (err, results) {
			console.log("error gen: %s", err)
			console.log("results text: %s", results)
			response.send("good");
			// response.send(results);
		});
	}
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


