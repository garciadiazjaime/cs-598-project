const AWS = require("aws-sdk");

AWS.config.update({region: 'us-west-2'});
const s3 = new AWS.S3({apiVersion: '2006-03-01'});

function uploadImageBase64(base64Data) {
  const buf = Buffer.from(base64Data, 'base64')
  const uploadParams = {
    Bucket: 'jaimeg4-food3', 
    Key: 'out.png', 
    Body: buf
  };

  return new Promise((resolve, reject) => {
    s3.upload(uploadParams, function (err, data) {
      console.log('s3.upload:start')
      if (err) {
        reject(err)
      } if (data) {
        console.log("Upload Success", data.Location);
        resolve(data.Location)
      }
    });

  })
}

exports.handler = async (event) => {
  if (event.body) {
    const body = JSON.parse(event.body)
    const base64Data = body.imageBase64.replace(/^data:image\/png;base64,/, "");
    await uploadImageBase64(base64Data)
  }

  const response = {
      statusCode: 200,
      headers: {
          "Access-Control-Allow-Headers" : "Content-Type",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
      },
      body: JSON.stringify('Hello from Lambda!'),
  };

  console.log('handler:end')
  return response;
};
