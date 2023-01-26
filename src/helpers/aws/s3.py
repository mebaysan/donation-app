import boto3
from botocore.config import Config


def get_presigned_url(bucket_name, object_name, expires_in=3600):
    # Apparently botocore still uses sigV2 by default, so we need to force it to use sigV4
    # source: https://github.com/boto/botocore/issues/2109#issuecomment-663155273

    boto_config = Config(
        signature_version='s3v4',
        region_name='eu-central-1'
    )

    # Create an S3 client
    s3 = boto3.client('s3', config=boto_config)

    # Generate the pre-signed URL
    response = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        },
        ExpiresIn=expires_in  # URL will be valid for 1 hour (default)
    )
    return response


def get_files_of_folder(bucket_name, file_prefix):
    # Apparently botocore still uses sigV2 by default, so we need to force it to use sigV4
    # source: https://github.com/boto/botocore/issues/2109#issuecomment-663155273
    boto_config = Config(
        signature_version='s3v4',
        region_name='eu-central-1'
    )

    # Create an S3 client
    s3 = boto3.client("s3", config=boto_config)

    # Use the S3 client to list all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=file_prefix)

    try:
        # Get the list of files from the response
        files = response['Contents']

        # Iterate through the list of files and get presigned urls
        files = [get_presigned_url(bucket_name, file['Key']) for file in files][
                1:]  # the first (0) element is the folder url, not a resource file
    except:
        # if there is exception, (probably) there is no image to show
        files = None

    return files


def get_folder_path_of_project_images(project_id):
    # our file path structure
    images_path = f"{project_id}/images/"
    return images_path


def get_folder_path_of_project_videos(project_id):
    # our file path structure
    videos_path = f"{project_id}/videos/"
    return videos_path
