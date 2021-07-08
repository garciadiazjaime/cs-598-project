const { RekognitionClient, DetectLabelsCommand } = require("@aws-sdk/client-rekognition");

function getLabels() {
  const client = new RekognitionClient({ region: "us-west-2" });
  const params = {
    Image: {
    S3Object: {
      Bucket: "jaimeg4-food3", 
      Name: "out.png"
    }
    }, 
    MaxLabels: 10, 
  };

  const command = new DetectLabelsCommand(params);

  return new Promise((resolve, reject) => {
    client.send(command).then(
      (data) => resolve(data),
      (error) => reject(error)
    );
  })  
}


exports.handler = async (event) => {
  const labels = await getLabels()

  const response = {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
      },
      body: JSON.stringify(labels)
  };

  return response;
};
