const verifyWebhook = (req, res) => {
  const VERIFY_TOKEN = 'ThislsAPrettybearbanana23token';
  console.log('Attempting to verify challenge');
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  console.log(mode);
  console.log(token);
  if (mode && token === VERIFY_TOKEN) {
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
};

module.exports = verifyWebhook;
