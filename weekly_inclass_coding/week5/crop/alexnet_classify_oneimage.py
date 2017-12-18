import math
import sys

from PIL import Image
from numpy import int32

sys.path.insert(0,'.')
sys.path.insert(0,'../imagenetdata')


from week5.thu.getimagenetclasses import *
from week5.thu.alexnet import *



def preproc_py2(imname,shorterside):
  
  
  pilimg = Image.open(imname)
  w,h=pilimg.size
  
  print((w,h))
  
  if w > h:
    longerside= np.int32(math.floor(float(shorterside)/float(h)*w))
    neww=longerside
    newh=shorterside
  else:
    longerside= np.int32(math.floor(float(shorterside)/float(w)*h))
    newh=longerside
    neww=shorterside    
  resimg=pilimg.resize((neww,newh))
  
  
  im = np.array(resimg,dtype=np.float32)
  
  

  return im
  
def cropped_center(im,hsize,wsize):
  h=im.shape[0]
  w=im.shape[1]
  
  cim=im[(h-hsize)/2:(h-hsize)/2+hsize,(w-wsize)/2:(w-wsize)/2+wsize,:]
  
  return cim
    

def preproc(image):
  
  '''
  filename_queue = tf.train.string_input_producer(
    tf.train.match_filenames_once("./images/*.jpg"))

  # Read an entire image file which is required since they're JPEGs, if the images
  # are too large they could be split in advance to smaller files or use the Fixed
  # reader to split up the file.
  image_reader = tf.WholeFileReader()
  
  # Read a whole file from the queue, the first returned value in the tuple is the
  # filename which we are ignoring.
  _, image_file = image_reader.read(filename_queue)
  
  '''
  
  height=tf.shape(image)[0]
  width=tf.shape(image)[1]
  new_shorter_edge=tf.cast(227, tf.int32)
  
  def _compute_longer_edge(height, width, new_shorter_edge):
    return tf.cast(width*new_shorter_edge/height, tf.int32)
  
  
  
  height_smaller_than_width = tf.less_equal(height, width)
  new_height_and_width = tf.cond(
    height_smaller_than_width,
    lambda: (new_shorter_edge, _compute_longer_edge(height, width, new_shorter_edge)),
    lambda: (_compute_longer_edge(width, height, new_shorter_edge), new_shorter_edge)
  )
  
  
  if image.dtype != tf.float32:
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
  
    
  resimg=tf.image.resize_images(
      image,
      new_height_and_width
      #tf.stack(new_height_and_width) #,
      #tf.concat(new_height_and_width)
      #method=ResizeMethod.BILINEAR,
      #align_corners=False
  )
  resimg = tf.expand_dims(resimg, 0)
  #image = tf.subtract(image, 110.0)

  return resimg



def run2():


  num_classes=1000
  batch_size=1
  keep_prob=1.
  skip_layer=[]
  is_training=False
  
  imagenet_mean = np.array([104., 117., 123.], dtype=np.float32) 
  
  cls=get_classes()
  
  sess = tf.Session()

  
  #imname='/home/binder/entwurf6/tfplaycpu/ai/alexnet/beach.jpg'
  imname='/home/binder/entwurf6/codes/tfplay/ai/alexnet/beach.jpg'

  
  #imname='/home/binder/entwurf6/tfplaycpu/ai/alexnet/poodle.png'
  #imname='/home/binder/entwurf6/tfplaycpu/ai/alexnet/quail227.JPEG'

  
  x = tf.placeholder(tf.float32, [batch_size, 227, 227, 3])
  net=AlexNet( x, keep_prob, num_classes, skip_layer, is_training, weights_path = 'DEFAULT')
  out=net.fc8
  
  
  init = tf.global_variables_initializer()
  sess.run(init)
  net.load_initial_weights(sess)
  
  
  
  
  
  im=preproc_py2(imname,250)
  print(im.shape)
  print(imname)
      
  if(im.ndim<3):
    im=np.expand_dims(im,2)
    im=np.concatenate((im,im,im),2)
      
  if(im.shape[2]>3):
    im=im[:,:,0:3]

  #here need to average over 5 crops instead of one
  imcropped=cropped_center(im,227,227)

  imcropped=imcropped[:,:,[2,1,0]] #RGB to BGR 
  imcropped=imcropped-imagenet_mean
  
  
  imcropped=np.expand_dims(imcropped,0)
  
  predict_values=sess.run(out, feed_dict={x: imcropped}  )
  
  
  
  print(('np.max(predict_values)', np.max(predict_values)))
  print(('classindex: ',np.argmax(predict_values)))
  print(('classlabel: ', cls[np.argmax(predict_values)]))

if __name__=='__main__':
  run2()
  #m=np.load('./ilsvrc_2012_mean.npy')
  #print(np.mean(np.mean(m,2),1))


