import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration       
cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API'), 
    api_secret = os.getenv('CLOUDINARY_SECRET'),
    secure=True
)

#Uploading a file on cloudinary
def uploadOnCloud(localPath:str, public_id = None):
    try:
        upload_result = cloudinary.uploader.upload(localPath, public_id = public_id)
        #now unlink file from local folder
        return upload_result
    except Exception as e:
        #now unlink file from local folder
        return e
    
