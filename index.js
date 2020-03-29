require('dotenv').config();
const express = require('express');

const app = express();
const port = 3000;
const {MessengerClient} = require('messaging-api-messenger');
// get accessToken from facebook developers website
// const client = MessengerClient.connect(process.env.ACCESS_TOKEN);
// Mock mode

const client = MessengerClient.connect({
  accessToken: process.env.ACCESS_TOKEN,
  origin: 'https://mockserver232sadf.com',
});

const bodyParser = require('body-parser');
const verifyWebhook = require('./src/validation/verifyWebhook');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

// Middleware
const getUser = require('./src/middleware/getUserContext');
app.use(getUser.getUserContext);


// Facebook validate application
app.get('/', verifyWebhook);

// Messenger bot callback
app.post('/', (req, res) => {
  console.log('Inserted here');
  const event = req.body.entry[0].messaging[0];
  const userId = event.sender.id;
  const {text} = event.message;
  client.sendText(userId, text);
  console.log(userId);
  res.send('Hello World!');
});



// client.sendText('3186769121397587', 'test');

// app.get('/', (req, res) => res.send('Hello World!'))
// dynamo.generateUser(req, res, 123123);

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
