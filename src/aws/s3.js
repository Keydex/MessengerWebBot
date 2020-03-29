const AWS = require('aws-sdk');
const uuid = require('node-uuid');
const bucketName = `node-sdk-sample-${uuid.v4()}`;
const keyName = 'hello_world.txt';
s3.createBucket({Bucket: bucketName}, function () {
    const params = {Bucket: bucketName, Key: keyName, Body: 'Hello World!'};
    s3.putObject(params, function (err) {
        if (err) console.log(err);
        else
            console.log(
                `Successfully uploaded data to ${bucketName}/${keyName}`
            );
    });
});