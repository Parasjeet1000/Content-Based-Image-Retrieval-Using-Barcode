import os
import numpy as np
from PIL import Image

database = os.listdir(os.path.join(os.getcwd(), 'MNIST_DS'))
pixel = 28


def average(l):
    return sum(l) / len(l)

def generate_c(p, avg):
    c = []
    for item in p:
        if item > avg:
            c.append(1)
        else:
            c.append(0)
    return c

def Barcode_Generator(querypath):
    projection1 = []
    projection2 = []
    projection3 = []
    projection4 = []

    image_path = querypath
    image = Image.open(image_path)
    arr = np.asarray(image)


    for i in range(pixel):
        projection1.append(arr[i][i])

        if i + 1 < pixel:
            projection3.append(arr[i][i + 1])
            projection4.append(arr[i + 1][i])

    projection2 = [sum(np.fliplr(arr).diagonal(1)), sum(np.fliplr(arr).diagonal(0)),
                    sum(np.fliplr(arr).diagonal(-1))]

    sum(projection1)
    col = [sum(x) for x in zip(*arr)]

    r_average = round(average(projection1), 0)

    c1 = generate_c(projection3, r_average)
    c2 = generate_c(projection4, r_average)
    c3 = generate_c(col, r_average)
    c4 = generate_c(projection2, r_average)
    #print('c1:', c1)
    #print('c2:', c2)
    #print('c3:', c3)
    #print('c4:', c4)
    barcode = c1 + c2 +  c3 + c4
    #print('Barcode:', barcode)

    return barcode

def hammingDistance(str1, str2):
    d = 0
    for c1, c2 in zip(str1, str2):  # zip() Iterate over several iterables in parallel
        if c1 != c2:
            d = d + 1
    return d


def Search_Algorithm(querypath):
    mindistance = 86 
    minpath = ''

    print('Searching for images similar to ' + querypath  + '.')
    
    for folder in database:
        
        folderpath = os.path.join(os.getcwd(), 'MNIST_DS/', folder)
        folderdir = os.listdir(folderpath)
        #print(folderpath)
        #print(folderdir)

        for image in folderdir:

            imagepath = os.path.join(os.getcwd(), 'MNIST_DS/' + folder, image)
            #print(querypath)
            #print(imagepath)
            #print(hammingDistance(Barcode_Generator(querypath),Barcode_Generator(imagepath)))

            if hammingDistance(Barcode_Generator(querypath),Barcode_Generator(imagepath)) < mindistance:
                mindistance = hammingDistance(Barcode_Generator(querypath),Barcode_Generator(imagepath))
                minpath = imagepath

    print('The closest match to the query image ' + querypath + ' was found at ' + minpath + '.')
    print('The Hamming distance between the two images is ' + str(mindistance) + '.')
    
querypath = os.path.join(os.getcwd(), 'Search', 'search.jpg')
Search_Algorithm(querypath)


