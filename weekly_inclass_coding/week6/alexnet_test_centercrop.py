import math
import sys

from PIL import Image

sys.path.insert(0, '.')
sys.path.insert(0, '../imagenetdata')

from week6.getimagenetclasses import *
from week6.alexnet import *


def preproc_py2(imname, shorterside):
    pilimg = Image.open(imname)
    w, h = pilimg.size

    print((w, h))

    if w > h:
        longerside = np.int32(math.floor(float(shorterside) / float(h) * w))
        neww = longerside
        newh = shorterside
    else:
        longerside = np.int32(math.floor(float(shorterside) / float(w) * h))
        newh = longerside
        neww = shorterside
    resimg = pilimg.resize((neww, newh))

    im = np.array(resimg, dtype=np.float32)

    return im


def cropped_center(im, hsize, wsize):
    h = im.shape[0]
    w = im.shape[1]

    cim = im[int((h - hsize) / 2):int((h - hsize) / 2 + hsize), int((w - wsize) / 2):int((w - wsize) / 2 + wsize), :]

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

    height = tf.shape(image)[0]
    width = tf.shape(image)[1]
    new_shorter_edge = tf.cast(227, tf.int32)

    def _compute_longer_edge(height, width, new_shorter_edge):
        return tf.cast(width * new_shorter_edge / height, tf.int32)

    height_smaller_than_width = tf.less_equal(height, width)
    new_height_and_width = tf.cond(
        height_smaller_than_width,
        lambda: (new_shorter_edge, _compute_longer_edge(height, width, new_shorter_edge)),
        lambda: (_compute_longer_edge(width, height, new_shorter_edge), new_shorter_edge)
    )

    if image.dtype != tf.float32:
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)

    resimg = tf.image.resize_images(
        image,
        new_height_and_width
        # tf.stack(new_height_and_width) #,
        # tf.concat(new_height_and_width)
        # method=ResizeMethod.BILINEAR,
        # align_corners=False
    )
    resimg = tf.expand_dims(resimg, 0)
    # image = tf.subtract(image, 110.0)

    return resimg


def getout():
    batchsize = 1
    is_training = False
    num_classes = 1000
    keep_prob = 1.
    skip_layer = []

    x = tf.placeholder(tf.float32, [batchsize, 227, 227, 3])
    net = AlexNet(x, keep_prob, num_classes, skip_layer, is_training, weights_path='DEFAULT')

    out = net.fc8

    return out, x, net


def run2():
    cstepsize = 20.0
    target_label = 949
    imname = 'C:\\Users\Hao\PycharmProjects\AI_Projects\week6\mon\imgs\img0.png'
    imname = 'C:\\Users\Hao\Desktop\\1.png'


    imagenet_mean = np.array([104., 117., 123.], dtype=np.float32)

    cls = get_classes()

    sess = tf.Session()

    out, x, net = getout()
    init = tf.global_variables_initializer()
    sess.run(init)
    net.load_initial_weights(sess)

    im = preproc_py2(imname, 250)
    print(im.shape)
    print(imname)

    # convert grey to color
    if (im.ndim < 3):
        im = np.expand_dims(im, 2)
        im = np.concatenate((im, im, im), 2)

    # dump alpha channel if it exists
    if (im.shape[2] > 3):
        im = im[:, :, 0:3]

    # here need to average over 5 crops instead of one
    image_croped = cropped_center(im, 227, 227)

    image_croped = image_croped[:, :, [2, 1, 0]]  # RGB to BGR
    image_croped = image_croped - imagenet_mean
    image_croped = np.expand_dims(image_croped, 0)
    print("Shape: ",type(image_croped),image_croped.shape)


    # run initial classification
    predict_values = sess.run(out, feed_dict={x: image_croped})

    original_label = np.argmax(predict_values)

    print('at start: classindex: ' + str(original_label) + '\nclasslabel: ' + cls[
        np.argmax(predict_values)] + '\nscore:' + str(np.max(predict_values)))

    print(predict_values[0,target_label],predict_values[0,original_label])

    print(image_croped[0].shape)
    img = Image.fromarray(image_croped[0],"RGB")
    img.save('C:\\Users\H\PycharmProjects\AI_Projects\week6\mon\imgs\modified_img0.png')
    img.show()


if __name__ == '__main__':
    run2()
    # m=np.load('./ilsvrc_2012_mean.npy')
    # print(np.mean(np.mean(m,2),1))
