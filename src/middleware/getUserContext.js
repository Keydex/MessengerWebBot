const dynamo = require('../aws/dynamo');

exports.getUserContext = async (req, res, next) => {
  // Check database if user exists
  console.log('Entered middleware');
  const event = req.body.entry[0].messaging[0];
  const userId = parseInt(event.sender.id, 10);
  if (await dynamo.verifyUserExists(userId)) {
    const result = await dynamo.getByID(userId);
    res.locals.userObj = result.data;
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
  res.locals.text = res.locals.event.text;
  console.log('Finished middleware');
  next();
};
