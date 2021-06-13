# -*- coding: utf-8 -*-
"""UNET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zw10a8qqnLmerdfIbmpk2LjLRyjlwfYp
"""

# 색상 코드 정의(32개)
color_codes = {
    'Animal':[64, 128, 64],
  'Archway':[192, 0, 128],
  'Bicyclist':[0, 128, 192],
  'Bridge':[0, 128, 64],
  'Building':[128, 0, 0],
  'Car':[64, 0, 128],
  'CartLuggagePram':[64, 0, 192],
  'Child':[192, 128, 64],
  'Column_Pole':[192, 192, 128],
  'Fence':[64, 64, 128],
  'LaneMkgsDriv':[128, 0, 192],
  'LaneMkgsNonDriv':[192, 0, 64],
  'Misc_Text':[128, 128, 64],
  'MotorcycleScooter':[192, 0, 192],
  'OtherMoving':[128, 64, 64],
  'ParkingBlock':[64, 192, 128],
  'Pedestrian':[64, 64, 0],
  'Road':[128, 64, 128],
  'RoadShoulder':[128, 128, 192],
  'Sidewalk':[0, 0, 192],
  'SignSymbol':[192, 128, 128],
  'Sky':[128, 128, 128],
  'SUVPickupTruck':[64, 128, 192],
  'TrafficCone':[0, 0, 64],
  'TrafficLight':[0, 64, 64],
  'Train':[192, 64, 128],
  'Tree':[128, 128, 0],
  'Truck_Bus':[192, 128, 192],
  'Tunnel':[64, 0, 64],
  'VegetationMisc':[192, 192, 0],
  'Void':[0, 0, 0],
  'Wall':[64, 192, 0] 
}

# MeanIou 함수 정의
class MeanIoU(object):

    def __init__(self, num_classes):
        super().__init__()

        self.num_classes = num_classes

    def mean_iou(self, y_true, y_pred):
      
        return tf.compat.v1.py_func(self._mean_iou, [y_true, y_pred], tf.float32)

    def _mean_iou(self, y_true, y_pred):
      
        """Computes the mean intesection over union using numpy.
        Args:
            y_true (tensor): True labels.
            y_pred (tensor): Predictions of the same shape as y_true.
        Returns:
            The mean intersection over union (np.float32).
        """
        # Compute the confusion matrix to get the number of true positives,
        # false positives, and false negatives
        # Convert predictions and target from categorical to integer format
        target = np.argmax(y_true, axis=-1).ravel()
        predicted = np.argmax(y_pred, axis=-1).ravel()

        # Trick for bincounting 2 arrays together
        x = predicted + self.num_classes * target
        bincount_2d = np.bincount(
            x.astype(np.int32), minlength=self.num_classes**2
        )
        assert bincount_2d.size == self.num_classes**2
        conf = bincount_2d.reshape(
            (self.num_classes, self.num_classes)
        )

        # Compute the IoU and mean IoU from the confusion matrix
        true_positive = np.diag(conf)
        false_positive = np.sum(conf, 0) - true_positive
        false_negative = np.sum(conf, 1) - true_positive

        # Just in case we get a division by 0, ignore/hide the error and
        # set the value to 1 since we predicted 0 pixels for that class and
        # and the batch has 0 pixels for that same class
        with np.errstate(divide='ignore', invalid='ignore'):
            iou = true_positive / (true_positive + false_positive + false_negative)
        iou[np.isnan(iou)] = 1

        return np.mean(iou).astype(np.float32)

"""### 모델 구성"""

from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, ReLU
from keras.layers import Conv2DTranspose, BatchNormalization, Dropout, Lambda

KERNEL = kernel = tf.keras.initializers.HeNormal()

def unet(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS, N_CLASSES):
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

    '''
    BatchNormalization(): 배치정규화 
    ReLu(): 활성화 함수 정의 
    Conv2D(): convolution layer 정의 (padding = 'same' : 입출력 이미지 사이즈 동일, kernel_initializer : 가중치 초기값을 he 정규분포로 초기화)
    MaxPooling2D(): max pooling 계층 정의
    Conv2DTranspose(): Conv2DTranspose 계층 정의(conv 연산을 역으로 계산)
    concat(): 각 출력 결과의 배열을 결합	
    '''

    # Encoder
    # conv2d layer
    c1 = Conv2D(64, (3, 3), padding='same', kernel_initializer=KERNEL)(inputs)
    c1 = ReLU()(c1)
    c1 = BatchNormalization()(c1)
    # conv2d_1 layer
    c1 = Conv2D(64, (3, 3), padding='same', kernel_initializer=KERNEL)(c1)
    c1 = BatchNormalization()(c1)
    c1 = ReLU()(c1)
    p1 = MaxPooling2D((2, 2), strides=2)(c1)
    
    # conv2d_2 layer
    c2 = Conv2D(128, (3, 3), padding='same', kernel_initializer=KERNEL)(p1)
    c2 = ReLU()(c2)
    c2 = BatchNormalization()(c2)
    # conv2d_3 layer
    c2 = Conv2D(128, (3, 3), padding='same', kernel_initializer=KERNEL)(c2)
    c2 = BatchNormalization()(c2)
    c2 = ReLU()(c2)
    p2 = MaxPooling2D((2, 2), strides=2)(c2)
    # conv2d_4 layer
    c3 = Conv2D(256, (3, 3), padding='same', kernel_initializer=KERNEL)(p2)
    c3 = ReLU()(c3)
    c3 = BatchNormalization()(c3)
    # conv2d_5 layer
    c3 = Conv2D(256, (3, 3), padding='same', kernel_initializer=KERNEL)(c3)
    c3 = ReLU()(c3)
    c3 = BatchNormalization()(c3)
    p3 = MaxPooling2D((2, 2), strides=2)(c3)
    # conv2d_6 layer
    c4 = Conv2D(512, (3, 3), padding='same', kernel_initializer=KERNEL)(p3)
    c4 = ReLU()(c4)
    c4 = BatchNormalization()(c4)
    # conv2d_7 layer
    c4 = Conv2D(512, (3, 3), padding='same', kernel_initializer=KERNEL)(c4)
    c4 = ReLU()(c4)
    c4 = BatchNormalization()(c4)
    p4 = MaxPooling2D((2, 2), strides=2)(c4)
    # conv2d_8 layer
    c5 = Conv2D(1024, (3, 3), padding='same', kernel_initializer=KERNEL)(p4)
    c5 = ReLU()(c5)
    c5 = BatchNormalization()(c5)

    # Decoder
    u6 = Conv2DTranspose(512, (2, 2), strides=2, padding='same')(c5)
    u6 = tf.concat([c4, u6], axis=3) 
    # conv2d_9 layer
    c6 = Conv2D(512, (3, 3), padding='same', kernel_initializer=KERNEL)(u6)
    c6 = ReLU()(c6)
    c6 = BatchNormalization()(c6)
    # conv2d_10 layer
    c6 = Conv2D(512, (3, 3), padding='same', kernel_initializer=KERNEL)(c6)
    c6 = ReLU()(c6)
    c6 = BatchNormalization()(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=2, padding='same')(c6)
    u7 = tf.concat([c3, u7], axis=3)
    # conv2d_11 layer
    c7 = Conv2D(256, (3, 3), padding='same', kernel_initializer=KERNEL)(u7)
    c7 = ReLU()(c7)
    c7 = BatchNormalization()(c7)
    # conv2d_12 layer
    c7 = Conv2D(256, (3, 3), padding='same', kernel_initializer=KERNEL)(c7)
    c7 = ReLU()(c7)
    c7 = BatchNormalization()(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=2, padding='same')(c7)
    u8 = tf.concat([u8, c2], axis=3)
    # conv2d_13 layer
    c8 = Conv2D(128, (3, 3), padding='same', kernel_initializer=KERNEL)(u8)
    c8 = ReLU()(c8)
    c8 = BatchNormalization()(c8)
    # conv2d_14 layer
    c8 = Conv2D(128, (3, 3), padding='same', kernel_initializer=KERNEL)(c8)
    c8 = ReLU()(c8)
    c8 = BatchNormalization()(c8)
    
    u9 = Conv2DTranspose(64, (2, 2), strides=2, padding='same')(c8)
    u9 = tf.concat([c1, u9], axis=3)
    # conv2d_15 layer
    c9 = Conv2D(64, (3, 3), padding='same', kernel_initializer=KERNEL)(u9)
    c9 = ReLU()(c9)
    c9 = BatchNormalization()(c9)
    # conv2d_16 layer
    c9 = Conv2D(64, (3, 3), padding='same', kernel_initializer=KERNEL)(c9)
    c9 = ReLU()(c9)
    c9 = BatchNormalization()(c9)

    # set outputs
    # conv2d_17 layer
    outputs = Conv2D(N_CLASSES, (1, 1), activation='softmax')(c9)
    model = Model(inputs=inputs, outputs=outputs)
    
    return model

"""### 모델 학습과정 설정"""

# MeanIoU 함수 적용
miou_metric = MeanIoU(N_CLASSES) 

# unet 함수 인자 정의
unet_model = unet(
    IMG_HEIGHT=NEW_SIZE[0], IMG_WIDTH=NEW_SIZE[1], IMG_CHANNELS=3,  N_CLASSES=N_CLASSES)

# unet 파라미터 정의
unet_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss = 'mean_squared_error',
    metrics=['accuracy', miou_metric.mean_iou])

# 모델 구조 확인
unet_model.summary()

"""### 모델 학습"""

EPOCHS = 100 # epoch 수 정의
BATCH_SIZE = 4 # batch_size 정의

# unet_model 모델 학습
history_unet = unet_model.fit(np.array(x_train), np.array(y_train),
                    validation_data=(np.array(x_val), np.array(y_val)), 
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    verbose=2)

"""### 학습 결과 시각화"""

'''
  train_loss_unet: 학습 데이터 loss 값
  train_accuracy_unet: 학습 데이터 accuracy 값
  train_miou_unet: 학습 데이터 mean_iou 값
  val_loss_unet: 검증 데이터 loss 값
  val_accuracy_unet: 검증 데이터 accuracy 값
  val_miou_unet: 검증 데이터 mean_iou 값
'''

train_loss_unet = history_unet.history['loss'] 
train_accuracy_unet = history_unet.history['accuracy']
train_miou_unet = history_unet.history['mean_iou']
val_loss_unet = history_unet.history['val_loss']
val_accuracy_unet = history_unet.history['val_accuracy']
val_miou_unet = history_unet.history['val_mean_iou']

# loss, accuracy, mean_iou 시각화(범위: epoch 수)
epoch = range(0, EPOCHS)

plt.figure(figsize=(23,8))
plt.subplot(1,3,1)
sns.lineplot(epoch, train_loss_unet)
sns.lineplot(epoch, val_loss_unet)
plt.title('Loss', size=14)
plt.legend(['train_loss', 'val_loss'])

plt.subplot(1,3,2)
sns.lineplot(epoch, train_accuracy_unet)
sns.lineplot(epoch, val_accuracy_unet)
plt.title('Accuracy', size=14)
plt.legend(['train_accuracy', 'val_accuracy'])

plt.subplot(1,3,3)
sns.lineplot(epoch, train_miou_unet)
sns.lineplot(epoch, val_miou_unet)
plt.title('Miou', size=14)
plt.legend(['train_miou', 'val_miou'])
plt.show()

"""### 테스트 데이터 예측 및 결과"""

# 테스트 데이터 예측
prediction_unet = unet_model.predict(np.array(x_test))

# 색상 코드 호출
color_codes_list = [color_codes[i] for i in color_codes.keys()]

# get_rgb_image 함수 정의
def get_rgb_image(prediction, n_classes, color_codes):
  
    '''
      output_height: 세로 크기(128) 정의
      output_width: 가로 크기(128) 정의
      seg_img: (128,128,3) shape 0으로 정의
   '''
    output_height = prediction.shape[0]
    output_width = prediction.shape[1]
    seg_img = np.zeros((output_height, output_width, 3))

    # 예측값에서 RGB 이미지를 반환
    for c in range(n_classes):
        seg_img[:, :, 0] += ((prediction[:, :, c])*(color_codes[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((prediction[:, :, c])*(color_codes[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((prediction[:, :, c])*(color_codes[c][2])).astype('uint8')
    return seg_img / 255.0

# 예측 이미지 시각화
for i in range(1,10):
    plt.figure(figsize=(15, 6))
    plt.subplot(1,3,1)
    plt.imshow(x_test[i])
    plt.title('Original Image')

    plt.subplot(1,3,2)
    plt.imshow(get_rgb_image(y_test[i], N_CLASSES, color_codes_list))
    plt.title('Labeled Image')
   
    plt.subplot(1,3,3)
    plt.imshow(get_rgb_image(prediction_unet[i], N_CLASSES, color_codes_list))
    plt.title('Predicted Image')
    plt.show()

# 테스트 데이터 MeanIou 값
unet_test_miou = tf.keras.metrics.MeanIoU(num_classes=32)
unet_test_miou.update_state(np.array(y_test), prediction_unet)
unet_test_miou.result().numpy()