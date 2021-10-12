import os
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from PIL import Image

global input_dir, output_dir, worklist, id, resolution
input_dir = './genshin'                 # the dir with all your pictures to be converted
output_dir = input_dir + '_webp/'       # the new output dir
worklist = []                           # address list for multi-processing
id = 0                                  # process counter
resolution = 512                        # output resolution

def image_process(file):
    global id, output_dir, resolution
    filepath_and_name, extname = os.path.splitext(file)
    if extname in ['.jpg','.jpeg','.png']:
        file_path, file_name_and_ext = os.path.split(file)
        file_name, extname = os.path.splitext(file_name_and_ext)
        outputfile = output_dir + file_name + '.webp'
        if os.path.exists(outputfile) == False :
            const_id = id
            id = id + 1
            print('Converting', const_id+1, '==>',file)
            im = Image.open(file)
            im.thumbnail((resolution,resolution))
            im.save(outputfile)
        else:
            pass
    else:
        pass
            
def file_walk(rootdir):
    global input_dir, worklist
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            worklist.append(os.path.join(root, file))

if __name__ == "__main__":
    print('Welcome to use WebP auto-converter!!')
    file_walk(input_dir)
    pool = Pool(cpu_count())
    pool.map(image_process, worklist)
    pool.close()
    pool.join()
    print('Report: Total', id, 'pictures are converted.')
