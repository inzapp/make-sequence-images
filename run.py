import os
import cv2
from time import time
from glob import glob
from tqdm import tqdm


index = 0
save_dir_name = f'{str(time()).replace(r".", "")}'
for path in tqdm(sorted(glob('*.jpg'), key=lambda x: int(''.join(filter(str.isdigit, x))))):
    label_path = f'{path[:-4]}.txt'
    if  not (os.path.exists(label_path) and os.path.isfile(label_path)):
        continue

    with open(label_path, 'rt') as f:
        lines = f.readlines()
    s = ''
    img = None
    raw_height, raw_width = 0, 0
    changed = False
    for line in lines:
        line = line.replace('\n', '')
        class_index, cx, cy, w, h = list(map(float, line.split()))
        class_index = int(class_index)
        if class_index == 0:
            if img is None:
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                raw_height, raw_width = img.shape[0], img.shape[1]
            x1 = cx - w / 2.0
            x2 = cx + w / 2.0
            y1 = cy - h / 2.0
            y2 = cy + h / 2.0

            x1 = int(x1 * raw_width)
            x2 = int(x2 * raw_width)
            y1 = int(y1 * raw_height)
            y2 = int(y2 * raw_height)

            sub = img[y1:y2, x1:x2]
            if not (os.path.exists(save_dir_name) and os.path.isdir(save_dir_name)):
                os.makedirs(save_dir_name, exist_ok=True)
            cv2.imwrite(f'{save_dir_name}/{index}.jpg', sub)
            index += 1
            class_index = 1
            changed = True
        s += f'{class_index} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n'
    if changed:
        with open(label_path, 'wt') as f:
            f.writelines(s)
