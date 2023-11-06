import time
import numpy as np

class ClassManager:
    def __init__(self, initial_observation_time, names, class_multipliers):
        self.start_time = time.time()
        self.initial_observation_time = initial_observation_time
        self.class_timestamps_list = []
        self.names = names
        self.class_multipliers = class_multipliers  
        self.rotate = 0
        self.first_list = []
        self.pin_list = []
        self.multiplier = 0
        self.safe_det_val = []
        self.rotation_increased = False

    def update_class_timestamps(self, det):
        if det is not None:
            self.class_timestamps_list.extend(det[:, 5].tolist())

    def reset_first_list(self):
        """Reset the first_list to an empty list."""
        self.first_list = []
        print("first_list has been reset.")

    def manage_classes(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time > self.initial_observation_time:
            classes, counts = np.unique(self.class_timestamps_list, return_counts=True)
            if len(counts) > 0:
                most_detected_class = classes[np.argmax(counts)]
                class_name = self.names[int(most_detected_class)]

                if class_name not in ["0deg", "30deg", "60deg", "90deg", "120deg", "150deg", "180deg"]:
                    self.pin_list.append(class_name)
                    if class_name == "Loose":
                        self.multiplier = 1
                    elif class_name == "Tight":
                        self.multiplier = 0.1
                    else:
                        self.multiplier = 0  # Reset to default value if not "Loose" or "Tight"

                    
                elif class_name not in ["Loose", "Tight"]:
                    self.first_list.append(class_name)
                    rotation_mapping = {
                        "0deg": "180deg",
                        "30deg": "0deg",
                        "60deg": "30deg",
                        "90deg": "60deg",
                        "120deg": "90deg",
                        "150deg": "120deg",
                        "180deg": "0deg"
                    }

                    if self.first_list[0] in rotation_mapping and class_name == rotation_mapping[self.first_list[0]]:
                        if not self.rotation_increased: 
                            self.rotate += 1
                            self.rotation_increased = True  
                            print(f"Rotate value increased to: {self.rotate}")
                    elif class_name != self.first_list[0]:
                        self.first_list = [class_name]  
                        print(f"The most detected class in the last 5 seconds is: {class_name}")

                self.class_timestamps_list = []
                self.start_time = time.time()
                print(f"Final Rotate Value: {self.rotate}")

        return self.rotate, self.multiplier
