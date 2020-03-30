/* eslint-disable max-classes-per-file */
const AWS = require('aws-sdk');
const uuid = require('node-uuid');
const User = require('../class/user');
const setError = require('../helper/error');
// Create a bucket and upload something into it

AWS.config.update({region: 'us-east-2'});
const ddb = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
const TableName = 'webcreator';

exports.createUser = async (user_id) => {
  const returnObject = {errors: []};
  const newUser = new User(parseInt(user_id, 10));
  const params = {
    TableName,
    Item: {
      USER_ID: newUser.user_id,
      data: newUser.export(),
    },
    ReturnValues: 'ALL_OLD',
  };
  // TODO: Find out how to properly return returnObject synchronously
  const result = await ddb
    .put(params, (err, data) => {
      if (err) {
        console.log('Error', err);
        returnObject.errors.push(setError('createUser', err));
      } else {
        console.log('Success', data);
        returnObject.data = data;
      }
    })
    .promise();
  console.log('CreateUser Result', result);
  return result;
};

exports.getByID = async (user_id) => {
  const returnObject = {errors: []};
  const params = {
    TableName,
    Key: {
      USER_ID: user_id,
    },
  };
  await ddb.get(params, (err, data) => {
    if (err) {
      console.log('Error', err);
      returnObject.errors.push(setError('createUser', err));
    } else {
      console.log('Success', data);
      returnObject.data = data.Item.data;
    }
  });

  return returnObject;
};

exports.verifyUserExists = async (user_id) => {
  const params = {
    TableName,
    Key: {
      USER_ID: user_id,
    },
  };
  await ddb.get(params, (err, data) => {
    if (err) {
      console.log('Error', err);
    } else {
      console.log("Weird validation", data);
      if (data.Item === undefined || data.Item.data === undefined) {
        return false;
      }
      return true;
    }
  });
};
