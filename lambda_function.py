import boto3
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.plot import reshape_as_raster


s3 = boto3.client('s3')

def getkey(messagetext,band):
    objectpath = messagetext['Records'][0]['s3']['object']['key']
    frags = objectpath.split('/')
    suffix = '_'+band+'.TIF'
    filename = frags[-2]+suffix
    filepath = '/'.join(frags[:-1])
    filepath = filepath+'/'+filename
    return filepath

def getbucketname(messagetext):
    bucketname = messagetext['Records'][0]['s3']['bucket']['name']
    return bucketname

def colorcorrect(x):
    return((x - np.nanmin(x))/(np.nanmax(x) - np.nanmin(x)))

def lambda_handler(event, context):
    rgbbands = ['B4','B3','B2'] #red,green,blue
    targetheight = 640
    targetwidth = 640
    imagestack = np.zeros((targetheight,targetwidth,len(rgbbands)))
    bucket = getbucketname(event)
    for count,band in enumerate(rgbbands): 
        key = getkey(event,band)
        resourceloc = 's3://'+bucket+'/'+key
        src = rasterio.open(resourceloc,GEOREF_SOURCES='INTERNAL')
        imagestack[:,:,count] = colorcorrect(src.read(1,out_shape=(targetheight, \
        targetwidth), resampling = Resampling.bilinear))
    np.clip(imagestack,0,1,out=imagestack)
    uintimage = (imagestack*255).astype(np.uint8)

    with rasterio.open('/tmp/Thumbnail_rast.png','w',driver='PNG', height=uintimage.shape[0],
    width=uintimage.shape[1], count=3, dtype=uintimage.dtype,) as outfile:
        outfile.write(reshape_as_raster(uintimage))
    s3.upload_file('/tmp/Thumbnail_rast.png', 'testpushkarbucket', 'Thumbnail_rast.png')