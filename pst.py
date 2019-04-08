import argparse
import os.path as osp
from config import *
import xml.etree.ElementTree as ET

VOC_ROOT = osp.join(HOME, "data/VOCdevkit/")

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_source', default=VOC_ROOT,
                    help='Dataset source directory path')
parser.add_argument('--classes', default=None, type=str,
                    help='The name of classes you want to extract, parse with symbol \',\'; you can select from ')
args=parser.parse_args()

#Classes Pretreatment
if args.classes == None:
    parser.error('Classes can not be empty!')
classeslist = args.classes.split(',')
#check if classes valid
classList_num=len(classeslist)
for i in range(classList_num):
    if (classeslist[i] in VOC_CLASSES) is False:
        parser.error('Invalid classes name {}'.format(classeslist[i]))
#get remained classes
ListAllClasses=list(VOC_CLASSES)
ListRemovedClasses=ListAllClasses
for i in range(classList_num):
    ListRemovedClasses.remove(classeslist[i])

#create path
VOC_2007=osp.join(args.dataset_source,'VOC2007')
VOC_Annotation=osp.join(VOC_2007,'Annotations')
VOC_ImageSets=osp.join(VOC_2007,'ImageSets')
VOC_ImageSets_Layout=osp.join(VOC_ImageSets,'Layout')
VOC_ImageSets_Main=osp.join(VOC_ImageSets,'Main')
VOC_ImageSets_Segmentation=osp.join(VOC_ImageSets,'Segmentation')
VOC_JPEGImages=osp.join(VOC_2007,'JPEGImages')
VOC_SegmentationClass=osp.join(VOC_2007,'SegmentationClass')
VOC_SegmentationObject=osp.join(VOC_2007,'SegmentationObject')
trainval_path=VOC_ImageSets_Main+'/'+'trainval.txt'
train_path=VOC_ImageSets_Main+'/'+'train.txt'
val_path=VOC_ImageSets_Main+'/'+'val.txt'
test_path=VOC_ImageSets_Main+'/'+'test.txt'
#imageset
for i in range(len(ListRemovedClasses)):
    x_train=VOC_ImageSets_Main+'/'+ListRemovedClasses[i]+'_train.txt'
    x_val=VOC_ImageSets_Main+'/'+ListRemovedClasses[i]+'_val.txt'
    x_trainval=VOC_ImageSets_Main+'/'+ListRemovedClasses[i]+'_trainval.txt'
    x_test=VOC_ImageSets_Main+'/'+ListRemovedClasses[i]+'_test.txt'
    if os.path.isfile(x_test):
        os.remove(x_test)
        print('[LOG]:{} is removed!'.format(x_test))
    if os.path.isfile(x_train):
        os.remove(x_train)
        print('[LOG]:{} is removed!'.format(x_train))
    if os.path.isfile(x_trainval):
        os.remove(x_trainval)
        print('[LOG]:{} is removed!'.format(x_trainval))
    if os.path.isfile(x_val):
        os.remove(x_val)
        print('[LOG]:{} is removed!'.format(x_val))

#read all classes  X_trainval/X_test.txt save number of pic used in future in num_set,num_list,num_tuple
num_set_test=set()#set of the classes that is used for train or test
num_set_trainval=set()
num_set_train=set()
num_set_val=set()
for i in range(len(classeslist)):#all classes
    classes_trainval=VOC_ImageSets_Main+'/'+classeslist[i]+'_trainval.txt'
    classes_train=VOC_ImageSets_Main+'/'+classeslist[i]+'_train.txt'
    classes_val=VOC_ImageSets_Main+'/'+classeslist[i]+'_val.txt'
    classes_test=VOC_ImageSets_Main+'/'+classeslist[i]+'_test.txt'
    if os.path.isfile(classes_test):
        file_object = open(classes_test,'rU')
        try: 
            for line in file_object:
                temp=line.split('\n')
                line_splited=temp[0].split(' ')
                if len(line_splited)==3 and (line_splited[2] =='1' or line_splited[2]=='0'):
                    num_set_test.add(line_splited[0])
        finally:
            file_object.close()

    if os.path.isfile(classes_trainval):
        file_object = open(classes_trainval,'rU')
        try: 
            for line in file_object:
                temp=line.split('\n')
                line_splited=temp[0].split(' ')
                if len(line_splited)==3 and (line_splited[2] =='1' or line_splited[2]=='0'):
                    num_set_trainval.add(line_splited[0])
        finally:
            file_object.close()
    if os.path.isfile(classes_train):
        file_object = open(classes_train,'rU')
        try: 
            for line in file_object:
                temp=line.split('\n')
                line_splited=temp[0].split(' ')
                if len(line_splited)==3 and (line_splited[2] =='1' or line_splited[2]=='0'):
                    num_set_train.add(line_splited[0])
        finally:
            file_object.close()
    if os.path.isfile(classes_val):
        file_object = open(classes_val,'rU')
        try: 
            for line in file_object:
                temp=line.split('\n')
                line_splited=temp[0].split(' ')
                if len(line_splited)==3 and (line_splited[2] =='1' or line_splited[2]=='0'):
                    num_set_val.add(line_splited[0])
        finally:
            file_object.close()
#fileIO used to fix train.txt val.txt trainval.txt or test.txt
def fixTrainORTestTxt(path,num_tuple):
    if os.path.isfile(path):
        with open(path,'r') as r:
            lines=r.readlines()
        with open(path,'w') as w:
            for l in lines:
                line_splited=l.split('\n')
                line_splited=line_splited[0].split(' ')
                if line_splited[0] in num_tuple:
                    w.write(l)
        

#get number tuple then  edit train.txt,test.txt,val.txt,trainval.txt
if len(num_set_test) is not 0:
    num_list_test=list(num_set_test)
    num_list_test.sort()
    num_tuple_test=tuple(num_list_test)
    fixTrainORTestTxt(test_path,num_tuple_test)
if len(num_set_train) is not 0:
    num_list_train=list(num_set_train)
    num_list_train.sort()
    num_tuple_train=tuple(num_list_train)
    fixTrainORTestTxt(train_path,num_tuple_train)
if len(num_set_val) is not 0:
    num_list_val=list(num_set_val)
    num_list_val.sort()
    num_tuple_val=tuple(num_list_val)
    fixTrainORTestTxt(val_path,num_tuple_val)
if len(num_set_trainval) is not 0:
    num_list_trainval=list(num_set_trainval)
    num_list_trainval.sort()
    num_tuple_trainval=tuple(num_list_trainval)
    fixTrainORTestTxt(trainval_path,num_tuple_trainval)
#fix XXX_test.txt,XXX_train.txt,XXX_val.txt,XXX_trainval.txt
for i in range(len(classeslist)):#all classes
    classes_trainval=VOC_ImageSets_Main+'/'+classeslist[i]+'_trainval.txt'
    classes_train=VOC_ImageSets_Main+'/'+classeslist[i]+'_train.txt'
    classes_val=VOC_ImageSets_Main+'/'+classeslist[i]+'_val.txt'
    classes_test=VOC_ImageSets_Main+'/'+classeslist[i]+'_test.txt'
    if os.path.isfile(classes_test):
        fixTrainORTestTxt(classes_test,num_tuple_test)
    if os.path.isfile(classes_trainval):
        fixTrainORTestTxt(classes_trainval,num_tuple_trainval)
    if os.path.isfile(classes_train):
        fixTrainORTestTxt(classes_train,num_tuple_train)        
    if os.path.isfile(classes_val):
        fixTrainORTestTxt(classes_val,num_tuple_val) 
#remove jpeg,segmentationClass,segmentationObject
DirTuple=(VOC_JPEGImages,VOC_SegmentationClass,VOC_SegmentationObject,VOC_Annotation)
for i in range(len(DirTuple)):
    list = os.listdir(DirTuple[i])
    for j in range(0,len(list)):
        path = osp.join(DirTuple[i],list[j])
        if os.path.isfile(path):
            file_name_list=list[j].split('.')
            if len(num_set_test) is not 0:
                if file_name_list[0] not in num_tuple_test:
                    os.remove(path)
            if len(num_set_trainval) is not 0:
                if file_name_list[0] not in num_tuple_trainval:
                    os.remove(path)
#edit xml
# ##2.remained xml remove other classes
list = os.listdir(VOC_Annotation)
for j in range(0,len(list)):
    path = osp.join(VOC_Annotation,list[j])
    tree = ET.parse(path)
    root = tree.getroot()
    node_remove=set()
    for obj in root.iter('object'):
        for name in obj.iter('name'):
            name_str=name.text
            if name_str not in classeslist:
                node_remove.add(obj)
    for i in node_remove:
        root.remove(i)
    tree.write(path)
