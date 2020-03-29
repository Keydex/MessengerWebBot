const dynamo = require('../aws/dynamo');

exports.getUserContext = async (req, res, next) => {
  // Check database if user exists
  console.log("Entered middleware");
  console.log(req.body);
  const event = req.body.entry[0].messaging[0];
  const userId = parseInt(event.sender.id, 10);
  console.log("more debug", event, userId);
  const result = await dynamo.getByID(userId);
  console.log(result);
  if (result.response.data) {
    res.locals.userObj = result.response.data;
  } else {
    res.locals.userObj = await dynamo.createUser(userId);
    console.log("Generated User with data", res.locals.userObj);
  }
  console.log("finished middleware")
  next();
};
