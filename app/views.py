from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import os
from tensorflow.python.ops import image_ops
from tensorflow.python.ops import io_ops
import numpy as np



# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = BASE_DIR + '/model'
model = tf.keras.models.load_model(model_path)


def index(request):

    return render(request, "app/index.html")


def predic(request):

    image = request.FILES['image-file']
    fs = FileSystemStorage()
    imagepath = fs.save(image.name, image)
    imagepath = fs.url(imagepath)
    test_image = '.'+imagepath
    print(test_image)
    #img = tf.keras.preprocessing.image.load_img(test_image)
    #x = tf.keras.preprocessing.image.img_to_array(img)
    #x = tf.data.Dataset.from_tensors(x)
    img = io_ops.read_file(test_image)
    img = image_ops.decode_image(
        img, channels=3, expand_animations=False)
    img = image_ops.resize_images_v2(img, (256, 256), method='bilinear')
    img.set_shape((256, 256, 3))
    x = tf.data.Dataset.from_tensors(img)
    x = x.batch(1)

    #x = x.batch(1)
    #data = next(iter(x))

    #img_path = os.path.join(BASE_DIR, 'media/photo')
    #img_path = os.path.dirname(img_path)
    # test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    #    img_path, color_mode='rgb', batch_size=1)

    result = model.predict(x)
    result_ph = np.asarray(result[0][0])
    result_normal = np.asarray(result[0][1])

    contex = {
        'result_ph': result_normal,
        'result_normal': result_ph,

    }
    return render(request, "app/predict.html", context=contex)
