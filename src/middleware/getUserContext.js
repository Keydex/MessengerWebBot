const dynamo = require('../aws/dynamo');

exports.getUserContext = async (req, res, next) => {
  // Check database if user exists
  console.log('Entered middleware');
  const event = req.body.entry[0].messaging[0];
  const userId = parseInt(event.sender.id, 10);
  const result = await dynamo.getByID(userId);
  if (result.Item !== undefined && result !== {}) {
    res.locals.userObj = result.Item.data;
    console.log('Successfully retrieved userData');
  } else {
    console.log('Creating new user');
    res.locals.userObj = await dynamo.createUser(userId).$response.data.Attributes;
    if (res.locals.userObj !== undefined) {
      console.log('Generated User with data', res.locals.userObj);
    } else {
      console.log('Caught Unknown Error, Inserting failed to DB');
    }
  }
  res.locals.event = event;
  res.locals.userId = userId;
  console.log('Finished middleware');
  next();
};
