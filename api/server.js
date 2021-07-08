const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const { RekognitionClient, DetectLabelsCommand } = require("@aws-sdk/client-rekognition");

const { uploadImageBase64 } = require('./s3');

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json({limit: '50mb'}))
app.use(cors())
 
app.get('/', function (req, res) {
  res.send('Hello World')
})

const client = new RekognitionClient({ region: "us-west-2" });

function getLabels() {
  return new Promise((resolve) => {
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

    client.send(command).then(
      (data) => resolve(data),
      (error) => resolve(error)
    );
  })  
}

app.post('/image', async(req, res) => {
  const base64Data = req.body.imageBase64.replace(/^data:image\/png;base64,/, "");

  uploadImageBase64(base64Data)

  const labels = await getLabels()

  res.send(labels)
})
 
app.listen(8080, () => {
  console.log('server running')
})
