require('dotenv').config();
const express = require('express');

const app = express();
const port = 3000;
const {MessengerClient} = require('messaging-api-messenger');
const bodyParser = require('body-parser');

// get accessToken from facebook developers website
const client = MessengerClient.connect(process.env.ACCESS_TOKEN);

// const client = MessengerClient.connect({
//   accessToken: process.env.ACCESS_TOKEN,
//   origin: 'https://mockserver232sadf.com',
// });

const verifyWebhook = require('./src/validation/verifyWebhook');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

// Middleware
const getUser = require('./src/middleware/getUserContext');


// Facebook validate application
app.get('/', verifyWebhook);

// Messenger bot callback
app.post('/', getUser.getUserContext, (req, res) => {
  console.log('Received Message from User!');
  console.log('information', res.locals.userId.toString(), res.locals.text);
  // client.sendText(res.locals.userId.toString(), res.locals.text);
  console.log('res.locals.userObj', res.locals.userObj);
  res.status(200).send(res.locals.userObj);
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
