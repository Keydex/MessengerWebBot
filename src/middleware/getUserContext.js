const dynamo = require('../aws/dynamo');
const User = require('../class/user');

exports.getUserContext = async (req, res, next) => {
  // Check database if user exists
  console.log('Entered middleware');
  const event = req.body.entry[0].messaging[0];
  const userId = parseInt(event.sender.id);
  const result = await dynamo.getByID(userId);
  if (result.Item !== undefined) {
    res.locals.userObj = result.Item.data;
    console.log('Successfully retrieved userData');
  } else {
    console.log('Creating new user');
    res.locals.userObj = new User(parseInt(userId, 10));
    await dynamo.createUser(res.locals.userObj);
  }
  res.locals.event = event;
  res.locals.userId = userId;
  
  res.locals.text = res.locals.event.text;
  console.log('Finished middleware');
  next();
};
