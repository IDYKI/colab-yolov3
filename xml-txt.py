import xml.etree.ElementTree as ET
from os import getcwd
import glob
from lxml import etree

classes = ["raccoon"]


def convert_annotation(image_id):
    in_file = open('./train_ann/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    txt_file = open('./txt/%s.txt'%(image_id), 'w')
    xml = open(r'{}'.format('./train_ann/%s.xml'%(image_id))).read()
    sel = etree.HTML(xml)
    width = int(sel.xpath('//size/width/text()')[0])
    height = int(sel.xpath('//size/height/text()')[0])
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (round(int(xmlbox.find('xmin').text)/width,4), round(int(xmlbox.find('ymin').text)/height,4),
             round(int(xmlbox.find('xmax').text)/width,4), round(int(xmlbox.find('ymax').text)/height,4))
        txt_file.write(str(cls_id) + " "+ " ".join([str(a) for a in b]) + ' ')


xmls = glob.glob('./train_ann/*.xml')
xmls_names = [x.split('\\')[-1].split('.xml')[0] for x in xmls]
for image_id in xmls_names:
    convert_annotation(image_id)
    
