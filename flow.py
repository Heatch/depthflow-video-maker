import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import requests

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())
    
def upload_file(file, subfolder="", overwrite=False):
    try:
        # Wrap file in formdata so it includes filename
        body = {"image": file}
        data = {}
        
        if overwrite:
            data["overwrite"] = "true"
  
        if subfolder:
            data["subfolder"] = subfolder

        resp = requests.post(f"http://{server_address}/upload/image", files=body,data=data)
        
        if resp.status_code == 200:
            data = resp.json()
            # Add the file to the dropdown list and update the widget value
            path = data["name"]
            if "subfolder" in data:
                if data["subfolder"] != "":
                    path = data["subfolder"] + "/" + path
            

        else:
            print(f"{resp.status_code} - {resp.reason}")
    except Exception as error:
        print(error)
    return path

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

def genImagePortrait(prompt, name):

    with open ("landscape_2ksampler_api.json", "r", encoding="utf-8") as f:
        flow_data = f.read()

    flow = json.loads(flow_data)

    #set the text prompt for our positive CLIPTextEncode
    seed = random.randint(0, 2**32 - 1)
    flow["3"]["inputs"]["seed"] = seed
    flow["10"]["inputs"]["seed"] = seed
    flow["6"]["inputs"]["text"] = prompt

    images = get_images(ws, flow)

    #Commented out code to display the output images:

    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            image.save(f"./images/{name}.png")

with open("test-output.json", "r", encoding="utf-8") as f:
    script = f.read()

script = json.loads(script)

counter = 1
total = len(script)
for image in script:
    genImagePortrait(image["image_prompt"], str(counter))
    print(f"Generated image {counter} of {total}")
    counter += 1
