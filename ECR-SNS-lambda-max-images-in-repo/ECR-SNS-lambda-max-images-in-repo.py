import boto3


def lambda_handler(event, context):

    client = boto3.client('ecr')
    image_list = []
    for data in client.list_images(repositoryName=event['detail']['repository-name'])['imageIds']:
        image_list.append(data['imageTag'])

    image_list.sort()
    print('Found images: '+ str(image_list))

    while len(image_list) > 10:
        response = client.batch_delete_image(
            repositoryName=event['detail']['repository-name'],
            imageIds=[
                {
                    'imageTag': image_list[0]
                },
            ]
        )
        image_list.remove(image_list[0])
        print(response)

    print('images left ' + str(image_list))
