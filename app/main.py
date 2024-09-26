
import torch
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
from fastapi import FastAPI, WebSocket
import time




# Load YOLO model (yolov5n is a lightweight model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', device='cpu')

# Create FastAPI app
myapp = FastAPI()

# Classes of interest (change as needed)
classes_of_interest = [0, 1, 3, 2, 5, 7, 9, 11, 15, 16, 17, 18, 19]

     
@myapp.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive the image bytes from the client
            image_bytes = await websocket.receive_bytes()

            # Convert the bytes to a PIL image using PIL
            image = Image.open(BytesIO(image_bytes))

            # Run the YOLO model on the image
            results = model(image)

            results.render()  
            img_buffer = BytesIO()
            Image.fromarray(results.ims[0]).save(img_buffer, format='JPEG')
            rendered_image_bytes = img_buffer.getvalue()
            await websocket.send_bytes(rendered_image_bytes)
           

            # Filter results by classes of interest
            # detected_objects = []
            # detected_objects_names = []
            # for pred in results.pred[0]:  # Loop over detections
            #     class_id = int(pred[-1])  # The class ID is the last value
            #     if class_id in classes_of_interest:
            #         detected_objects.append({
            #             'class': model.names[class_id],
            #             'confidence': float(pred[4]),  # Confidence score
            #             'bbox': [float(pred[0]), float(pred[1]), float(pred[2]), float(pred[3])]  # Bounding box
            #         })
            #         detected_objects_names.append(model.names[class_id])

            # # Send the detection results back to the client as JSON
            # await websocket.send_json({'detections': detected_objects_names})

    except Exception as e:
        await websocket.send_text(e)
        print(f"Error: {e}")