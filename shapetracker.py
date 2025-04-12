import cv2
import numpy as np
from kalmanfilter import KalmanFilter


class ShapeTracker:
    def __init__(self):
        self.tracked_objects = []  #tracked objects
        self.miss_threshold = 5  # Frames to keep undetected objects(if misses more than 5 deletes)

    def detect_shapes(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)  # Thresholding
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find shapes

        detected_shapes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)  # Calculate contour area
            if area < 500:  # Filter small contours (reduce noise)
                continue

            shape = self._classify_shape(cnt)  # Identify shape
            center = self._get_contour_center(cnt)  # Calculate center
            detected_shapes.append({'center': center, 'contour': cnt, 'type': shape})

        return detected_shapes

    def _classify_shape(self, contour):
        peri = cv2.arcLength(contour, True)  # Calculate perimeter
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)  # Simplify contour
        sides = len(approx)  # Count vertices

        if sides == 3:
            return "triangle"
        elif sides == 4:
            x, y, w, h = cv2.boundingRect(approx)
            return "square" if 0.9 <= w / h <= 1.1 else "rectangle"  # Check aspect ratio
        else:
            return "circle"

    def _get_contour_center(self, contour):
        M = cv2.moments(contour)  # Calculate moments
        if M["m00"] == 0: return (0, 0)  # division by zero problem
        return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  # Calculate centroid

    def update_tracking(self, detected_shapes):
        # Predict existing objects
        for obj in self.tracked_objects:
            obj['kalman'].predict()  # Predict next position
            obj['misses'] += 1  # Increment undetected count

        # Match detections to tracked objects
        for detection in detected_shapes:
            closest = None
            min_dist = 50  # Maximum association distance

            for obj in self.tracked_objects:
                dist = np.linalg.norm(np.array(detection['center']) - obj['kalman'].position)
                if dist < min_dist:  # Find nearest tracked object
                    min_dist = dist
                    closest = obj

            if closest:  # Update existing tracker
                closest['kalman'].correct(np.array([detection['center']], dtype=np.float32).T)
                closest['contour'] = detection['contour']
                closest['type'] = detection['type']
                closest['misses'] = 0  # Reset undetected counter

        # Add new objects
        for detection in detected_shapes:
            if not any(np.linalg.norm(np.array(detection['center']) - obj['kalman'].position) < 50
                       for obj in self.tracked_objects):  # Check if new detection
                self.tracked_objects.append({  # Create new tracker
                    'kalman': KalmanFilter(detection['center']),
                    'contour': detection['contour'],
                    'type': detection['type'],
                    'misses': 0
                })

            # Remove old objects
            self.tracked_objects = [obj for obj in self.tracked_objects if obj['misses'] < self.miss_threshold]

    def draw_results(self, frame):
        for obj in self.tracked_objects:
            cv2.drawContours(frame, [obj['contour']], -1, (0, 255, 255), 2)  # Draw contour
            x, y = obj['kalman'].position
            cv2.putText(frame, f"{obj['type']} ({x},{y})",  # Add label
                        (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)