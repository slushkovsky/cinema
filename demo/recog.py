import os
import json
from collections import namedtuple

import cv2
import numpy as np
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier


Seat = namedtuple('Seat', ['tl', 'br']) 
Point = namedtuple('Point', ['x', 'y'])

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Predictor(object):
    PREDICT_OCCUPIED = 1
    PREDICT_FREE = 2

    STND_SIZE = (20, 30)

    def __init__(self, model_path, marking):
        assert isinstance(marking, list)

        self.model=joblib.load(model_path)
        self.marking = marking
     
    def predict(self, img):
        for seat in self.marking:
            sample = img[seat.tl.y:seat.br.y, seat.tl.x:seat.br.x] # NOTE: Get seat ROI

            sample = cv2.resize(sample, self.STND_SIZE)
            sample = np.reshape(sample, (1, sample.shape[0] * sample.shape[1]))

            yield self.model.predict(sample)[0]
                 

def load_marking(filepath): 
    with open(filepath, 'r') as f: 
        _marking = json.load(f)
        
    marking = []
    
    for seat in _marking:
        marking.append(Seat(
            tl=Point(seat['tl']['x'], seat['tl']['y']),
            br=Point(seat['br']['x'], seat['br']['y'])
        ))
    
    return marking
        

def recog_video(filepath): 
    marking = load_marking(os.path.join(CURRENT_DIR, 'marking.json'))
    predictor = Predictor(os.path.join(CURRENT_DIR, 'model_v2.pkl'), marking) 
    
    cap = cv2.VideoCapture(filepath) 

    seats_count = len(marking)

    accumulated = [0] * seats_count

    frame_count = 0

    while True: 
        ret, img = cap.read() 

        if not ret: 
            break

        frame_count += 1
        print(frame_count)

        if len(img.shape) > 2: 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        predict = list(predictor.predict(img))

        for i, item in enumerate(predict):
            accumulated[i] += item

        if frame_count > 100: 
            break

    return ['free' if round(item / seats_count) == 1 else 'occupied'  for item in accumulated]
    

if __name__ == '__main__': 
    marking = load_marking(os.path.join(CURRENT_DIR, 'marking.json'))
    predictor = Predictor(os.path.join(CURRENT_DIR, 'model_v2.pkl'), marking) 

    test_img = cv2.imread(os.path.join(CURRENT_DIR, '2.jpg'))

    if len(test_img.shape) > 2:
        test_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)


    from pprint import pprint; pprint(list(predictor.predict(test_img)))
