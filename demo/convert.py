import json
import sys
import os

import dill


if __name__ == '__main__':
    filepath = os.path.realpath(sys.argv[1])
    data = []

    with open(filepath, 'rb') as f:
        old_data = dill.load(f)

    assert len(old_data) % 2 == 0
        
    for i in range(0, len(old_data), 2):
        tl = old_data[i]
        br = old_data[i + 1]

        data.append({
            'tl': {
                'x': tl[0],
                'y': tl[1]
            },
            'br': {
                'x': br[0],
                'y': br[1]
            }
        })

    save_path = '.'.join(filepath.split('.')[:-1]) + '.json'

    with open(save_path, 'w') as f:
        json.dump(data, f)

        
        
