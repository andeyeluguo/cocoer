# cityscapes imports
from cityscapesscripts.helpers.annotation import Annotation
from cityscapesscripts.helpers.labels import labels, name2label
import glob
import os
import shutil
import pdb


def mkdir(path):
    if os.path.exists(path):
        print('have exists')
    else:
        os.makedirs(path)
if __name__ == '__main__':

    imgDir = 'VOCdevkit/JPEGImages/'
    annDir = 'VOCdevkit/Annotations/'
    createDir = False
    if createDir:
        mkdir(imgDir)
        mkdir(annDir)
        #file process
        png_files = glob.glob('leftImg8bit/train/*/*png')
        png_files = png_files + glob.glob('leftImg8bit/val/*/*png')
        json_files = glob.glob('gtFine/train/*/*json')
        json_files = json_files + glob.glob('gtFine/val/*/*json')
        for i in range(len(png_files)):
            shutil.move(png_files[i], imgDir + str(i) + '.png')
            shutil.move(json_files[i], annDir + str(i) + '.json')
        shutil.rmtree('./gtFine')
        shutil.rmtree('./leftImg8bit')
            
    #content process
    traffic_objects = ['traffic light', 'traffic sign', 'person', 'rider', 'car', 'truck','bus', 'motorcycle', 'bicycle']
    json_files = glob.glob(annDir+'/*json')
    for json_file in json_files:
        annotation = Annotation()
        annotation.fromJsonFile(json_file)
        width =  annotation.imgWidth
        height = annotation.imgHeight
        #pdb.set_trace()
        file_name = json_file.split('\\')[1].split('.')[0]
        xml_file = open(annDir + file_name + '.xml', 'w')
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>./</folder>\n')
        xml_file.write('    <filename>' + imgDir + file_name + '.png' + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')        
        xml_file.write('    </size>\n')            
        
        for obj in annotation.objects:
            #core
            label   = obj.label
            polygon = obj.polygon
            
            #special
            if obj.deleted:
                continue
            isGroup = 0
            if ( not label in name2label ) and label.endswith('group'):
                label = label[:-len('group')]
                isGroup = 1
                
            if not label in name2label:
                printError( "Label '{}' not known.".format(label) )
            
            if label in traffic_objects: #change to voc
                xmin = polygon[0][0]
                xmax = polygon[0][0]
                ymin = polygon[0][1]
                ymax = polygon[0][1]
                for i in range(1, len(polygon)):
                    if xmin > polygon[i][0]:
                        xmin = polygon[i][0]
                    if xmax < polygon[i][0]:
                        xmax = polygon[i][0]
                    if ymin > polygon[i][1]:
                        ymin = polygon[i][1]
                    if ymax < polygon[i][1]:
                        ymax = polygon[i][1]
                xml_file.write('    <object>\n')
                xml_file.write('        <name>' + label + '</name>\n')
                xml_file.write('        <pose>Unspecified</pose>\n')
                xml_file.write('        <truncated>0</truncated>\n')
                xml_file.write('        <difficult>0</difficult>\n')
                xml_file.write('        <iscrowd>' + str(isGroup)+ '</iscrowd>\n')
                xml_file.write('        <bndbox>\n')
                xml_file.write('            <xmin>' + str(xmin) + '</xmin>\n')
                xml_file.write('            <ymin>' + str(ymin) + '</ymin>\n')
                xml_file.write('            <xmax>' + str(xmax) + '</xmax>\n')
                xml_file.write('            <ymax>' + str(ymax) + '</ymax>\n')
                xml_file.write('        </bndbox>\n')
                xml_file.write('    </object>\n') 
        xml_file.write('</annotation>')
        xml_file.close()
