import boto3
import pprint
pp = pprint.PrettyPrinter(indent=4)

def upload_imaget_to_bucket():
  s3 = boto3.resource('s3')

  for bucket in s3.buckets.all():
    print(bucket.name)
  
  data = open('../images/test/dessert/2468099496096536383.jpg', 'rb')
  s3.Bucket('jaimeg4-food3').put_object(Key='2468099496096536383.jpg', Body=data)

def is_food(data):
  for row in data['Labels']:
    if row['Name'] == 'Food' and row['Confidence'] > 50:
      return True
  
  return False

def main():
  client = boto3.client('rekognition')  
  response = client.detect_labels(
    Image={
        'S3Object': {
          'Bucket': 'jaimeg4-food3',
          'Name': '2468099496096536383.jpg',
        }
    },
    MaxLabels=15,
  )
  pp.pprint(response)

  if is_food(response):
    print("is food, yummi!")
  else:
    print("is not food :(")

if __name__ == "__main__":
  main()
