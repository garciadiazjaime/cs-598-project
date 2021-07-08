const AWS = require("aws-sdk");
const fs = require('fs');

AWS.config.update({region: 'us-west-2'});
const s3 = new AWS.S3({apiVersion: '2006-03-01'});

const fileName = 'out.png'

function uploadImage() {
  const file = `${fileName}`
  const fileStream = fs.createReadStream(file);

  fileStream.on('error', (err) => {
    console.log('File Error', err);
  });

  const uploadParams = {
    Bucket: 'jaimeg4-food3', 
    Key: fileName, 
    Body: fileStream
  };

  s3.upload(uploadParams, function (err, data) {
    if (err) {
      console.log("Error", err);
    } if (data) {
      console.log("Upload Success", data.Location);
    }
  });
}

function uploadImageBase64(base64Data) {
  const buf = Buffer.from(base64Data, 'base64')

  const uploadParams = {
    Bucket: 'jaimeg4-food3', 
    Key: fileName, 
    Body: buf
  };

  s3.upload(uploadParams, function (err, data) {
    if (err) {
      console.log("Error", err);
    } if (data) {
      console.log("Upload Success", data.Location);
    }
  });
}

function getCredentials() {
  AWS.config.getCredentials((err) => {
    if (err) console.log(err.stack)
    // credentials not loaded
    else {
      console.log("Access key:", AWS.config.credentials.accessKeyId)
    }
  })
}

function listBuckets() {
  s3.listBuckets(function(err, data) {
    if (err) {
      console.log("Error", err);
    } else {
      console.log("Success", data.Buckets);
    }
  });
}

async function main() { 
  getCredentials()

  // listBuckets()

  uploadImage()
}


// main()

module.exports = {
  uploadImage,
  uploadImageBase64
}
