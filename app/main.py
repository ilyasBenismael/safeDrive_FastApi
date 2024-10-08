import torch
from fastapi import FastAPI, WebSocket
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


# Load YOLO model (yolov5n is a lightweight model)
yoloModel = torch.hub.load('ultralytics/yolov5', 'yolov5n', device='cpu')  

# Create FastAPI app
myapp = FastAPI()


@myapp.websocket("/yolo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("midas to yolo accepted")
    a = 0

    try:
        while True:
            received_message = await websocket.recv()
            print("received from midas")

            a += 1
            await websocket.send(f"hey abooood : {a}")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send(f"yolo error : {e}")
        await websocket.close()

    
            # Receive the image bytes from the client
            # image_bytes = await websocket.receive_bytes()

            # # Convert bytes to a NumPy array for YOLO
            # nparr = np.frombuffer(image_bytes, np.uint8)
            # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # # Apply YOLO inference
            # results = yoloModel(img)

            # print("got results")

            # results.render()

            # rendered_img = results.ims[0].copy()

            # # turn the numpy img to bytes
            # img_buffer = BytesIO()
            # Image.fromarray(rendered_img).save(img_buffer, format='JPEG')
            # rendered_image_bytes = img_buffer.getvalue()

            # # send image bytes back via websocket
            # await websocket.send_bytes(rendered_image_bytes)


######################################################################################""
           

                    
            # detected_objects = []
            # # Iterate over each prediction
            # for pred in results.xyxy[0]:
            #     x1, y1, x2, y2, confidence, class_id = pred
                
            #     # Filter out objects with confidence less than 0.35
            #     if confidence >= 0.35:
            #         # Get the class name from the class_id
            #         class_name = yoloModel.names[int(class_id)]
                    
            #         # Add the object to the detected_objects list as a dictionary
            #         detected_objects.append({
            #             'class_name': class_name,
            #             'coordinates': [x1.item(), y1.item(), x2.item(), y2.item()],
            #             'confidence': confidence.item()
            #         })



























            # #loop on detected objcts and for each one get the className, and get the meandepth of bbox then print it
            # for pred in results.xyxy[0]:      
            #     x1, y1, x2, y2, confidence, class_id = pred
                   
            #     depth_values = midasNumpy[int(y1):int(y2)+1, int(x1):int(x2)+1]
            #     mean_depth = np.nanmean(depth_values)        
            #     mean_depth_str = f"{mean_depth:.2f}"
        
            #     # Add the mean_depth text at the top of the bounding box
            #     cv2.putText(rendered_img, mean_depth_str, (int(x2), int(y2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
