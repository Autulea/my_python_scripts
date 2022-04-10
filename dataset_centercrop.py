import os
import re
from PIL import Image

input_dir = './pic/'
output_dir ='./dataset/'
worklist = []
resolution = 512
finished = 0

def file_walk(dir=input_dir):
    global worklist
    for root, dirs, files in os.walk(dir):
        for file in files:
            worklist.append(os.path.join(root, file))

def image_cropper(img_path: str):
    global finished, output_dir, resolution
    filepath_and_name, extname = os.path.splitext(img_path)
    if extname in ['.webp']:
        file_path, file_name_and_ext = os.path.split(img_path)
        file_name, extname = os.path.splitext(file_name_and_ext)
        tags = re.split(' ', file_name_and_ext)
        outputfile = output_dir + tags[1] + '.jpg'
        if os.path.exists(outputfile) == False and os.path.getsize(img_path) < 1.5e6:
            im = Image.open(img_path)
            im = im.convert('RGB')
            if min(im.size[0], im.size[1]) >= 512:
                if im.size[0] == im.size[1]:
                    im.thumbnail((resolution, resolution))
                elif im.size[0] < im.size[1]:
                    height = int(resolution * im.size[1] / im.size[0])
                    im = im.resize((resolution, height))
                    start = int((height - resolution) / 2)
                    im = im.crop((0, start, resolution, start + resolution))
                elif im.size[0] > im.size[1]:
                    width = int(resolution * im.size[0] / im.size[1])
                    im = im.resize((width, resolution))
                    start = int((width - resolution) / 2)
                    im = im.crop((start, 0, start + resolution, resolution))
                im.save(outputfile)
                finished += 1
                print(finished, file_name)


if __name__ == "__main__":
    file_walk()
    for img in worklist:
        image_cropper(img)


