/* eslint-disable max-classes-per-file */
const AWS = require('aws-sdk');
const uuid = require('node-uuid');

const s3 = new AWS.S3();
// Create a bucket and upload something into it

AWS.config.update({region: 'us-east-2'});
const ddb = new AWS.DynamoDB.DocumentClient();
const TableName = 'webcreator';

exports.createUser = async (user_id) => {
  const newUser = new User(parseInt(user_id, 10));
  const params = {
    TableName,
    Item: {
      USER_ID: newUser.user_id,
      data: newUser.export(),
    },
  };
  console.log(params);
  ddb.put(params, (err, data) => {
    if (err) {
      console.log('Error', err);
    } else {
      console.log('Success', data);
    }
  });
};

exports.getByID = async (user_id) => {
  const params = {
    TableName,
    Item: {
      USER_ID: user_id,
    },
  };
  return ddb.get(params, (err, data) => {
    if (err) {
      console.log('Error', err);
    } else {
      console.log('Success', data);
    }
  });
};
