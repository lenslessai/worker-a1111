import time
import runpod
import os
import requests
from requests.adapters import HTTPAdapter, Retry
from my_utils import dir_size_in_mb, remove_3_oldest_files, download_model 

LOCAL_URL = "http://127.0.0.1:3000/sdapi/v1"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


# ---------------------------------------------------------------------------- #
#                              Automatic Functions                             #
# ---------------------------------------------------------------------------- #
def wait_for_service(url):
    '''
    Check if the service is ready to receive requests.
    '''
    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(0.2)


def run_inference(inference_request):
    '''
    Run inference on a request.
    '''

    print("inference_request:\n")
    print(inference_request)
    api_name = inference_request["api_name"]
    api_method = inference_request["api_method"]
    lora_model_name = inference_request["lora_model_name"]
    user_id = inference_request["user_id"]

    lora_model_name_in_volume = user_id + "_" + lora_model_name
    if dir_size_in_mb("/runpod-volume") > 8000:
      remove_3_oldest_files("/runpod-volume/models/Lora")

    if not os.path.exists(lora_model_name_in_volume):
      download_model(user_id, lora_model_name, lora_model_name_in_volume)

     
    inference_request["a1111_body"]["prompt"] += " <lora:"+ lora_model_name_in_volume + ":1>"
    if api_method == "GET":
        response = automatic_session.get(url=f'{LOCAL_URL}/{api_name}', timeout=600)
    else:
        response = automatic_session.post(url=f'{LOCAL_URL}/{api_name}', json=inference_request["a1111_body"], timeout=600)

    return response.json()


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''

   
    json = run_inference(event["input"])

    # return the output that you want to be returned like pre-signed URLs to output artifacts
    return json


if __name__ == "__main__":
    wait_for_service(url=f'{LOCAL_URL}/txt2img')

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler})
