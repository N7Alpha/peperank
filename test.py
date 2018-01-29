import basc_py4chan
import urllib.request
import time
import os
import subprocess
import dhash
from wand.image import Image

pepes = []

def add_pepe(image_url):
    duplicate = False
    with Image(filename=imageUrl) as image:
        row, col = dhash.dhash_row_col(image)
        for n in range(len(pepes)):
            if dhash.get_num_bits_different(pepes[n][0][0], row) + dhash.get_num_bits_different(pepes[n][0][1], col) < 2:
                pepes[n][2] += 1
                duplicate = True
    if not duplicate:
        pepes.append([[row,col],image_url,1])


def label_image(image_url):
    ret = subprocess.run(['python3', './label_image.py', '--graph=./output_graph.pb', '--labels=./retrained_labels.txt', '--image=' + image_url, '--input_layer=input', '--output_layer=final_result', '--input_mean=128', '--input_std=128', '--input_width=192', '--input_height=192'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if ret == 'PEPE':
        return True

boardNames = ['tv', 'b', 'v', 'r9k']
alreadyCollectedThumbnails = set()
count = 0
pepeCount = 0
logCount = 1
while True:
    for boardName in boardNames:
        text_file = open("log" + str(logCount) + ".txt", "w")
        for pepe in pepes:
            text_file.write("File: " + pepe[1] + "     " + "Count: " + str(pepe[2]) + "\n");
        text_file.close()
        logCount += 1
        board = basc_py4chan.Board(boardName)
        thread_ids = board.get_all_thread_ids()
        str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works



        for thread_id in thread_ids:
            thread = board.get_thread(thread_id)
            if thread is not None:
                thumbnailUrls = [x for x in thread.thumbs()]
                imageUrls = [x for x in thread.files()]

                for n in range(len(thumbnailUrls)):
                    thumb = thumbnailUrls[n]
                    imageUrl = imageUrls[n]
                    if thumb not in alreadyCollectedThumbnails:
                        alreadyCollectedThumbnails.add(thumbnailUrls[n]);
                        urllib.request.urlretrieve(thumb, "./thumbnails/thumb" + str(count) + ".jpg")
                        if label_image("./thumbnails/thumb" + str(count) + ".jpg"):
                            urllib.request.urlretrieve(imageUrl, "./pepes/pepe" + str(pepeCount) + imageUrl[-4:])
                            if label_image("./pepes/pepe" + str(pepeCount) + imageUrl[-4:]):
                                pepeCount += 1;
                                add_pepe("./pepes/pepe" + str(pepeCount) + imageUrl[-4:])
                            else:
                                os.remove("./pepes/pepe" + str(pepeCount) + imageUrl[-4:])
                        count += 1

    time.sleep(60 * 5)
