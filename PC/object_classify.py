import cv2
import numpy as np
import openvino as ov

class ObjectClassification:
    def __init__(self, model_xml_path):
        core = ov.Core()

        model = core.read_model(model=model_xml_path)

        self.compiled_model = core.compile_model(model=model, device_name='CPU')
        
        self.output_layer = self.compiled_model.output(0)
        
    def __del__(self):
        print("Object Classification 클래스 종료")
        pass
    
    def classify(self, frame):
        image = frame

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize to MobileNet image shape.
        input_image = cv2.resize(src=image, dsize=(224, 224))

        # Reshape to model input shape.
        input_image = np.expand_dims(input_image, 0)
        input_image = np.swapaxes(input_image, 1, 3)
        input_image = np.swapaxes(input_image, 2, 3)

        result_infer = self.compiled_model([input_image])[self.output_layer]
        result_index = np.argmax(result_infer)

        return result_index