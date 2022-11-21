import string
import numpy as np
import tensorflow as tf
import cv2
import os

class CRNNWordPredicter:

    def __init__(self):
        
        file_dir = os.path.dirname(__file__)
        model_file_name = os.path.join(file_dir,'cnn_rnn_20.h5')
        self.crnn_model = tf.keras.models.load_model(model_file_name, compile=False)

    def predict_from_img(self, img):
        '''
        Make a prediction with the crnn model on the image and returns a human-readable string 
        '''
        preprocessed_img = self._preprocess_img(img)
        prediction = self.crnn_model(preprocessed_img)
        return self._decode(prediction)

    def _preprocess_img(self, img):
        '''
        Preprocess the img for the prediction. 
        It applies a thresholding to remove noise and then resize the img to the size on which the model was trained
        '''
        t, img_preprocessed = cv2.threshold(img,120,255, type = cv2.THRESH_BINARY) 
        img_preprocessed = cv2.resize(img, (128,32))/255
        img_preprocessed = tf.expand_dims(img_preprocessed, -1)
        img_preprocessed = tf.expand_dims(img_preprocessed, 0)
        return img_preprocessed

    def _decode(self, prediction, char_list = list(string.printable)):
        '''
        Transform the prediction to a human-readable string
        '''
        # ctc beam search decoder
        predicted_codes, _ = tf.nn.ctc_greedy_decoder(
            # shape of tensor [max_time x batch_size x num_classes]
            tf.transpose(prediction, (1, 0, 2)),
            [prediction.shape[1]]*prediction.shape[0]
        )

        # convert to int32
        codes = tf.cast(predicted_codes[0], tf.int32)

        # Decode the index of caracter
        table = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(
                    np.arange(len(char_list)),
                    char_list,
                    key_dtype=tf.int32
                ),
                '',
                name='id2char'
            )
        text = table.lookup(codes)

        # Convert a SparseTensor to string
        text = tf.sparse.to_dense(text).numpy().astype(str)

        return list(map(lambda x: ''.join(x), text))[0]