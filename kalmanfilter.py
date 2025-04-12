import cv2
import numpy as np


class KalmanFilter:
    def __init__(self, initial_position):
        self.kf = cv2.KalmanFilter(4, 2)  # Creates a Kalman Filter(x,y,dx,dy)

        # Transition matrix (linear motion only)
        self.kf.transitionMatrix = np.array([  # Models object movement (constant velocity)
            [1, 0, 1, 0],  # x_new = x + dx*dt (dt=1)
            [0, 1, 0, 1],  # y_new = y + dy*dt
            [0, 0, 1, 0],  # dx remains same
            [0, 0, 0, 1]], dtype=np.float32)  # dy remains same

        # Measurement matrix
        self.kf.measurementMatrix = np.array([  # Maps state to measurements
            [1, 0, 0, 0],  # Only measures x position
            [0, 1, 0, 0]], dtype=np.float32)  # Only measures y position

        # Covariance matrices
        self.kf.processNoiseCov = 1e-4 * np.eye(4, dtype=np.float32)  # Uncertainty in motion model
        self.kf.measurementNoiseCov = 1e-1 * np.eye(2, dtype=np.float32)  # Sensor noise
        self.kf.errorCovPost = np.eye(4, dtype=np.float32)  # Initial error covariance

        # Initial state
        self.kf.statePost = np.array([  # Initial values for state vector
            [initial_position[0]],  # Initial x
            [initial_position[1]],  # Initial y
            [0],  # Initial x-velocity
            [0]], dtype=np.float32)  # Initial y-velocity

    def predict(self):
        return self.kf.predict()  # Predict next state

    def correct(self, measurement):
        self.kf.correct(measurement)  # Update with actual measurement

    @property
    def position(self):
        return self.kf.statePost[:2].flatten().astype(int)  # Get current estimated (x,y)