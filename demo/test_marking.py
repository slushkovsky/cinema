import os
import json

import cv2


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__': 
    img = cv2.imread(os.path.join(CURRENT_DIR, '2.jpg'))

    with open('marking.json', 'r') as f: 
        marking = json.load(f)

    for seat in marking:
        cv2.rectangle(img, (seat['tl']['x'], seat['tl']['y']), (seat['br']['x'], seat['br']['y']), (255, 0, 0))
    
    cv2.imwrite('marking_test.jpg', img) 
