const dynamo = require('../aws/dynamo');

exports.getUserContext = async (req, res, next) => {
  // Check database if user exists
  const event = req.body.entry[0].messaging[0];
  const userId = event.sender.id;
  const result = await dynamo.getByID(userId);
  console.log(result);
  if (result) {
    res.locals.userObj = result;
  } else {
    res.locals.userObj = await dynamo.generateUser(userId);
  }
  next();
};
