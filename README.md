# Semantic-Segmentation

## :raising_hand: Participant
- 김서희[rlawjdghl456@naver.com]
- 서민지[jaaaamj0711@gmail.com]
- 이채윤[dbs8438@gmail.com]

## :information_desk_person: Introduce
University of Cambridged에서 제공하는 CamVid 데이터셋을 사용하여 Semantic-Segmentation을 진행하였습니다. 해당 데이터셋은 주행하면서 얻은 거리 수준 뷰가 들어있는 영상 모음으로 자동차, 도로등을 포함하여 총 32개의 클래스에 대한 픽셀 수준의 레이블이 담겨있습니다.  

데이터에 대한 자세한 설명은 다음 [사이트](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/)에서 확인할 수 있습니다.

<img width="812" alt="스크린샷 2021-06-13 오후 6 35 41" src="https://user-images.githubusercontent.com/55734436/121802187-31e17b00-cc76-11eb-9b56-7819ff2cbe5e.png">

다음과같이 Orginal 데이터를 Labeled 데이터로 분류하는 것이 프로젝트의 목표입니다. 

## :scissors: Data preprocessing
<img width="983" alt="스크린샷 2021-06-13 오후 10 57 00" src="https://user-images.githubusercontent.com/55734436/121810173-b6de8b80-cc9a-11eb-8981-f174c8b1fb70.png">

- cv2.imread 함수를 사용하여 데이터를 읽어올시 BGR형태로 데이터가 바뀌게 됩니다. 따라서 cvt.cvtColor함수를 사용하여 원본 데이터인 RGB형태로 변경합니다.
- 원본 데이터의 크기는 (720,960,3)입니다. 학습 시 속도 향상의 효율성을 위해 cv2에서 제공하는 resize 함수를 사용하여 (128,128,3)로 사이즈를 변경합니다.

Labeled 데이터도 다음과 동일하게 전처리를 진행합니다.

## :hammer: Usage model
- FCN
- U-NET
- SEGNET

## :open_file_folder: Project structure
```
|--Data
|  |--Original_data        # original 데이터
|  |--Labeled_data        # labeled 데이터 
  
    |--Preprocessing
    |  |--preprocessing.py    # 데이터 전처리 

        |--Modeling      
        |  |--fcn.py     # fcn 모델
        |  |--unet.py    # unet 모델
        |  |--segnet.py  # segnet 모델
```

## :computer: Requirements
```
numpy == 1.19.5
pandas == 1.1.5
scikit-learn == 0.22.2
tensorflow == 2.5.0
keras == 2.5.0
cv2 == 4.1.2
```
## :bulb: Result

### Train/Validation Loss, Accracy, Miou

<img width="900" height = "250" alt="a" src="https://user-images.githubusercontent.com/55734436/121809657-9d3c4480-cc98-11eb-872f-0d3464316951.png">
<img width="900" height = "250" alt="a" src="https://user-images.githubusercontent.com/55734436/121809664-a0cfcb80-cc98-11eb-9967-0e6eee456b35.png">

### Predicted Image Example
<img alt="a" src="https://user-images.githubusercontent.com/55734436/121809770-189df600-cc99-11eb-9f92-3bc76a28d0c3.png">
<img alt="a" src="https://user-images.githubusercontent.com/55734436/121809775-1cca1380-cc99-11eb-8db8-784076260ca6.png">



