/* eslint-disable max-classes-per-file */
const AWS = require('aws-sdk');
const uuid = require('node-uuid');
const User = require('../class/user');
const setError = require('../helper/error');
// Create a bucket and upload something into it

AWS.config = new AWS.Config();
AWS.config.accessKeyId = process.env.AWS_ACCESS_KEY;
AWS.config.secretAccessKey = process.env.AWS_SECRET_KEY;
AWS.config.region = "us-east-2";
const ddb = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
const TableName = 'webcreator';

exports.createUser = async (userObj) => {
  const params = {
    TableName,
    Item: {
      USER_ID: userObj.user_id,
      data: userObj,
    },
  };
  // TODO: Find out how to properly return returnObject synchronously
  const response = await ddb
    .put(params, (err, data) => {
      if (err) {
        console.log('Error -', err);
      } else {
        console.log('Success - new user created', data);
      }
    }).promise();
  console.log('CreateUser Result', response);
  return await response;
};

exports.getByID = async (user_id) => {
  const params = {
    TableName,
    Key: {
      USER_ID: user_id,
    },
    ConsistentRead: true,
  };
  let response = await ddb.get(params, (err, data) => {
    if (err) {
      console.log(err)
    } else {
      console.log(data);
    }
  }).promise();
  console.log(response);
  return await response;
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
