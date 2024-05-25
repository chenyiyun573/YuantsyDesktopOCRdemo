import json
import os
import dotenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

dotenv.load_dotenv()  # Load environment variables from .env file

def get_ocr_results(image_url):
    try:
        # Load credentials from environment variables
        SecretId = os.getenv("SECRET_ID")
        SecretKey = os.getenv("SECRET_KEY")
        cred = credential.Credential(SecretId, SecretKey)

        # Setup HTTP and client profile
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        # Create OCR client
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        # Prepare request
        req = models.GeneralBasicOCRRequest()
        params = {"ImageUrl": image_url, "IsPdf": True}
        req.from_json_string(json.dumps(params))

        # Execute request and return results
        resp = client.GeneralBasicOCR(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        return str(err)

# Example call
# print(get_ocr_results("hhttp://public.yuantsy.com/PDF_Split/CS188/31.pdf"))
