from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("images/car.jpg", save=True)

print("Detection Complete")