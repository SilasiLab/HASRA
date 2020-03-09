import keras
import os
import keras.backend as K
from data_utils import prepare_for_training
import numpy as np
import cv2
from keras.preprocessing.image import ImageDataGenerator
class Detector():
    def __init__(self, weights_path="None"):
        self.weights_path = None
        if os.path.exists(weights_path):
            self.weights_path = weights_path
        self.model = self.get_model()

    def get_model(self):
        '''
        Input shape = (224, 224, 3)
        '''
        input_shape = (224, 224, 3)
        input = keras.layers.Input(shape=input_shape)
        x = keras.applications.mobilenet_v2.MobileNetV2(include_top=False, weights='imagenet')(input)
        x = keras.layers.GlobalMaxPooling2D()(x)

        # x = keras.layers.Dense(512)(x)
        # x = keras.layers.BatchNormalization()(x)
        # x = keras.layers.Activation('relu')(x)
        #
        # x = keras.layers.Dense(1024)(x)
        # x = keras.layers.BatchNormalization()(x)
        # x = keras.layers.Activation('relu')(x)

        output = keras.layers.Dense(1, activation='sigmoid')(x)
        model = keras.Model(inputs=[input], outputs=[output])
        if self.weights_path:
            model.load_weights(self.weights_path)
        opt = keras.optimizers.Adam()
        loss = keras.losses.binary_crossentropy
        metric = keras.metrics.binary_accuracy
        model.compile(optimizer=opt, loss=loss, metrics=[metric])
        model.summary()
        return model

    def train(self, x, y, batch_size=32, epoch=50, split=0.1):
        te_index = int(x.shape[0] * split)
        teX, teY = x[0: te_index], y[0: te_index]
        trX, trY = x[te_index:], y[te_index:]

        datagen = ImageDataGenerator(
            featurewise_center=False,
            featurewise_std_normalization=False,
            rotation_range=5,
            width_shift_range=0.1,
            height_shift_range=0.1,
            vertical_flip=True,
            zoom_range=[0.8, 1.2],
            brightness_range=[0.5, 1.2],
            rescale=1./255.
        )
        datagen.fit(x)
        callBackList = []
        callBackList.append(keras.callbacks.ModelCheckpoint("model/model.h5", save_best_only=True))
        step_per_epoch = int(trX.shape[0] / batch_size)
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        self.model.fit_generator(datagen.flow(trX, trY, batch_size=batch_size), steps_per_epoch=step_per_epoch, epochs=epoch,
                                 callbacks=callBackList, validation_data=test_datagen.flow(teX, teY, batch_size=32), validation_steps=20)
        # for x_batch, y_batch in datagen.flow(trX, trY, batch_size=1):
        #     print(y_batch[0])
        #     cv2.imshow('1', x_batch[0])
        #     cv2.waitKey(0)
    def predict(self, images):
        result = self.model.predict(images)
        return result

    def predict_on_single_raw_image(self, opencv_image):
        predict_image = np.asarray([cv2.resize(opencv_image, (224, 224))])
        predict_image = predict_image / 255.
        return self.model.predict(predict_image)[0]

    def predict_in_real_use(self, opencv_image):
        predict_image = np.asarray([cv2.resize(opencv_image, (224, 224))])
        predict_image = predict_image / 255.
        result = self.model.predict(predict_image)[0]
        # cv2.imshow('pred', opencv_image)
        # cv2.waitKey(0)
        print(result)
        if result < 0.5:
            return True
        return False

def test_on_video(video_file):
    video_stream = cv2.VideoCapture(video_file)
    grab, frame = video_stream.read()
    d = Detector("model/model.h5")
    while frame is not None:
        result = d.predict_on_single_raw_image(frame)
        cv2.putText(frame,"Confidence: %.4f" % result, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), lineType=cv2.LINE_AA)
        if result > 0.5:
            cv2.putText(frame, "Display" % result, (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                        lineType=cv2.LINE_AA)
        else:
            cv2.putText(frame, "Keep still" % result, (340, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                        lineType=cv2.LINE_AA)
        cv2.imshow("test_on_video", frame)
        cv2.waitKey(0)
        grab, frame = video_stream.read()

if __name__ == '__main__':
    # d = Detector()
    # output_folder = "/mnt/4T/pellet_output"
    # x, y = prepare_for_training(output_folder)
    # print(x.shape)
    # print(y.shape)
    #
    # d.train(x, y)
    #
    # print(d.predict(x[0: 10, :, : ,:]))
    # print(y[0: 10])
    test_on_video("/mnt/4T/pellet_test/2020-01-16_(07-00-33)_002FBE71E101_85136_12744.avi")