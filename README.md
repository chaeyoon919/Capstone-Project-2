# Semantic-Segmentation
캡스톤 프로젝트2 과목을 수강하며 진행했던 프로젝트입니다.

## Participant
- 김서희
- 서민지
- 이채윤

## Introduce
University of Cambridged에서 제공하는 CamVid 데이터셋을 사용하여 Semantic-Segmentation을 진행하였습니다. 해당 데이터셋은 주행하면서 얻은 거리 수준 뷰가 들어있는 영상 모음으로 자동차, 도로등을 포함하여 총 32개의 클래스에 대한 픽셀 수준의 레이블이 담겨있습니다.
<img width="812" alt="스크린샷 2021-06-13 오후 6 35 41" src="https://user-images.githubusercontent.com/55734436/121802187-31e17b00-cc76-11eb-9b56-7819ff2cbe5e.png">

다음과같이 Orginal 데이터를 Labeled 데이터로 분류하는 것이 프로젝트의 목표입니다. 


## Usage model
- FCN
- U-NET
- SEGNET

## Project structure
```
|--Data
|  |--Original_data        # original 데이터
|  |--Labeled_data        # labeled 데이터 
  
    |--Preprocessing
    |  |--jpreprocessing.py    # 데이터 전처리 

        |--Modeling      
        |  |--fcn.py     # fcn 모델
        |  |--unet.py    # unet 모델
        |  |--segnet.py  # segnet 모델

```
