import cv2
import socket
import openvino as ov

from object_classify import ObjectClassification

# N,C,H,W = batch size, number of channels, height, width.
H, W = 736, 992

# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = "127.0.0.1"
server_port = 3000
server_addr_port = (server_ip, server_port)

class ObjectDetection:
    def __init__(self):
        self.object_list = ["Human", "Car", "Plane"]
        # Define colors for boxes and descriptions.
        self.colors = {"red": (255, 0, 0), "green": (0, 255, 0)}
        self.send_flag = 0
        
        # model_xml_path = "./otx_v1/otx-workspace-DETECTION/outputs/export/openvino.xml"
        model_xml_path = "../model/detection/v1/openvino.xml"

        core = ov.Core()

        model = core.read_model(model=model_xml_path)

        self.compiled_model = core.compile_model(model=model, device_name="CPU")
        
        # self.input_layer_ir = self.compiled_model.input(0)
        self.output_layer_ir = self.compiled_model.output("boxes")
        self.label_layer_ir = self.compiled_model.output("labels")
        
    def __del__(self):
        print("Object Detection 클래스 종료")
        pass
    
    def send_message(self, msg):
        bytes_to_send = str.encode(msg)    
        udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_client_socket.sendto(bytes_to_send, server_addr_port)
    
    def obj_detect(self, bgr_image, resized_image, input_image, threshold=0.5, conf_labels=True):
        boxes = self.compiled_model([input_image])[self.output_layer_ir]
        boxes = boxes[0]
        labels = self.compiled_model([input_image])[self.label_layer_ir]
        label = labels[0]
        
        # Fetch the image shapes to calculate a ratio.
        (real_y, real_x), (resized_y, resized_x) = bgr_image.shape[:2], resized_image.shape[:2]
        ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

        # Convert the base image from BGR to RGB format.
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        label_index = 0
        # Iterate through non-zero boxes.
        for box in boxes:
            # Pick a confidence factor from the last place in an array.
            conf = box[-1]
            if conf > threshold:
                # Convert float to int and multiply corner position of each box by x and y ratio.
                # If the bounding box is found at the top of the image, 
                # position the upper box bar little lower to make it visible on the image. 
                (x_min, y_min, x_max, y_max) = [
                    int(max(corner_position * ratio_y, 10)) if idx % 2 
                    else int(corner_position * ratio_x)
                    for idx, corner_position in enumerate(box[:-1])
                ]

                # Draw a box based on the position, parameters in rectangle function are: image, start_point, end_point, color, thickness.
                rgb_image = cv2.rectangle(rgb_image, (x_min, y_min), (x_max, y_max), self.colors["green"], 3)

                # Add text to the image based on position and confidence.
                # Parameters in text function are: image, text, bottom-left_corner_textfield, font, font_scale, color, thickness, line_type.
                if conf_labels:
                    rgb_image = cv2.putText(
                        rgb_image,
                        f"{self.object_list[label[label_index]]}, {conf:.2f}",
                        (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        self.colors["red"],
                        2,
                        cv2.LINE_AA,
                    )
                mid = int((x_max - x_min) / 2 + x_min)
                
                if self.send_flag == 0:
                    if mid < 200:
                        if label[label_index] == 0:
                            print("Human Detected !!!")
                            self.send_message("0")
                            self.send_flag = 1
                        elif label[label_index] == 1:
                            print("Car Detected !!!")
                            
                            model_xml_path = "../model/classification/car_v1/openvino.xml"
                                    
                            objClassify = ObjectClassification(model_xml_path)
                            crop_image = rgb_image[y_min:y_max, x_min:x_max]
                            object_index = objClassify.classify(crop_image)
                            self.send_message(str(object_index))
                            print("send classification message::",object_index)
                            self.send_flag = 1
                            del objClassify
                        elif label[label_index] == 2:
                            print("Plane Detected !!!")
                            
                            model_xml_path = "../model/classification/plane_v1/openvino.xml"
                                    
                            objClassify = ObjectClassification(model_xml_path)
                            crop_image = rgb_image[y_min:y_max, x_min:x_max]
                            object_index = objClassify.classify(crop_image)
                            self.send_message(str(object_index))
                            print("send classification message::",object_index)
                            self.send_flag = 1
                            del objClassify
                        #print("****",mid)
                elif self.send_flag == 1:
                    if 300 < mid < 340:
                        self.send_message("9")
                        print("send stop message")
                        self.send_flag = 0
                        #print(mid)

            label_index = label_index + 1

        rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        return rgb_image