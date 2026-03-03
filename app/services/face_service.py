import face_recognition
import numpy as np
import cv2
from typing import List, Optional
from fastapi import HTTPException, status

class FaceService:
    @staticmethod
    def process_image(image_bytes: bytes) -> np.ndarray:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file format")
        small_frame = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        return rgb_small_frame

    @staticmethod
    def get_face_encoding(image_bytes: bytes) -> List[float]:
        rgb_image = FaceService.process_image(image_bytes)
        face_locations = face_recognition.face_locations(rgb_image)
        if len(face_locations) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face found in image")
            
        if len(face_locations) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Multiple faces found. Please provide an image with only 1 face.")
            
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        return face_encodings[0].tolist()
        
   
    @staticmethod
    def verify_face(known_encoding: List[float], image_bytes: bytes, tolerance: float = 0.45) -> bool:
        known_face_encodings = [np.array(known_encoding)]
        rgb_image = FaceService.process_image(image_bytes)
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face found in image")
        
        if len(face_locations) > 1:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Multiple faces found. Only 1 face allowed for login.")
             
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0], tolerance=tolerance)
        return matches[0]

