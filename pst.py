import argparse
import os.path as osp
from config import *


VOC_ROOT = osp.join(HOME, "data/VOCdevkit/")
VOC_DST = osp.join(HOME, "dst/VOCdevkit/")

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_source', default=VOC_ROOT,
                    help='Dataset source directory path')
parser.add_argument('--dataset_dst', default=VOC_DST,
                    help='Subdataset destination directory path')
parser.add_argument('--classes', default=None, type=str,
                    help='The name of classes you want to extract, parse with symbol \',\'; you can select from ')
args=parser.parse_args()

#####classes####
classeslist = args.classes.split(',')
print(classeslist)