
# 🚀 표적 탐지 미사일 자동화 시스템
## 🚩 프로젝트 소개 
![](https://velog.velcdn.com/images/jimeaning/post/607480bd-88ce-44d8-ae55-8583f6038a54/image.png)

**표적을 감지하여 알맞은 미사일 선택 후 올바른 각도와 세기로 격파하는 시스템**이다.
줄어드는 청년 인구에 따른 군 인력 문제를 해결하기 위한 타겟 포착 및 분석 자동화 적 섬멸 시스템

- **프로젝트 기간** : 23/12/18 ~ 24/01/16
- **프로젝트 인원** : 4인
- **프로젝트 기능**
	- 180도로 카메라가 돌면서 표적 탐지
	- 표적이 탐지되면 detection과 classification 수행
	- 표적의 특성에 따라 포 선택 후 해당 무기 LED 점화 (강도, 속도 등)
	- PI제어로 계산된 각도로 포 제어
	- 표적을 화면 중앙에 위치시킨 후 카운트다운 시작
	- 발사 후 시스템 재정비

### 🦿 개발 동기 및 필요성
![image](https://github.com/jimeaning/BTS/assets/62744644/ced902e1-4e87-41a3-a3bd-d85c86589b5b)

- 국방에서도 기계화되는 움직임이 늘어나고 있다. 최근 인구 감소로 인해 군 병력 인원이 줄었고, 기술의 발전이 원인이다. 기계화를 통해 CCTV 등 인원을 효율적으로 간소화시킬 수 있으며 사람이 놓친 정보를 기계가 포착하는 등 협업이 가능해진다.
- 자동화 격추 시스템을 통해 출동할 인원이 부족하거나 제약이 있을 때, 통제실에서 감시, 탐지, 결정, 준비, 발사 모든 과정을 수행할 수 있다.
- 감시 및 탐지 과정에는 두 가지 경우가 나올 수 있다.
(1) 표적을 확실히 detect를 했을 때
사람은 기계가 정하는 타이밍에 따라 결정을 내리면 된다.
(2) 표적이 애매하게 detected 되었을 때
완전한 자동화와 부분적 자동화의 문제가 있다. 컴퓨터의 판단과 사람의 개입 중 각각의 효율성과 정확도이 어느정도 되는지 판단되어야 한다. 완전 자동화의 가능성이 궁금해 시작하게 된 프로젝트이다.

### 🦿 High Level Design

- **Sequence Diagram**

![](https://velog.velcdn.com/images/jimeaning/post/e3ffa80a-ba46-4fc5-9d02-969eba477bf9/image.png)

- **Class Diagram**

![image](https://github.com/jimeaning/BTS/assets/62744644/cdae17cc-fc73-495a-9611-3314cca90495)

- **통신 Sequence**
![image](https://github.com/jimeaning/BTS/assets/62744644/4325ec3f-ddf0-40e1-8881-cabab186c258)

- **Multi Thread Processing**
  
![multithread](https://github.com/jimeaning/BTS/assets/62744644/3f6404a7-5e79-4f58-9366-97973bf34265)

### 🦿 시스템 아키텍처
![image](https://github.com/jimeaning/BTS/assets/62744644/fa4de51c-99dd-4ee0-a929-7398ae921d40)

**RaspberryPi**
-   HW 모듈 제어
-   서버와 GUI에서 메시지를 수신 받아 처리
-   서버로 웹캠 프레임 전송
-   GUI로 발사 버튼 활성화 메시지 전송
-   C++, CMake, make 사용

**RaspberryPi - 회로도**
![image](https://github.com/jimeaning/BTS/assets/62744644/9435d382-7699-4fbc-8034-92761cadb0b6)

## 🚩 Server
![image](https://github.com/jimeaning/BTS/assets/62744644/5153d5be-0e0a-42b9-a036-9ebded0ecc7e)
![image](https://github.com/jimeaning/BTS/assets/62744644/d3bfe7c0-bd66-4328-a5cc-6d6f5160ade8)

### 🦿 Class Diagram
![image](https://github.com/jimeaning/BTS/assets/62744644/21bdae1d-8937-4390-a6a8-5996c4e5f787)


### 🦿 Object Detection
![image](https://github.com/jimeaning/BTS/assets/62744644/425d37dd-21c5-40f4-948b-18c33ee8d66e)

### 🦿 Classification
![image](https://github.com/jimeaning/BTS/assets/62744644/b33947c0-bff2-45a8-8c25-7545692a6be8)

## 🚩 User
![](https://velog.velcdn.com/images/jimeaning/post/9a70e703-063e-4b44-bd65-ac3c2f61e0d6/image.png)
-   서버로 부터 Inferencing된 이미지 수신
-   HW로부터 동작 메시지 수신
-   HW로 발사 명령 송신

### 🦿 Class Diagram
![image](https://github.com/jimeaning/BTS/assets/62744644/25bfe350-cc4b-430b-bed1-a6c373b2983b)


## 🚩 Output
### 🚶‍♀️ Client
**Object Detection 후 Classification까지 마친 상태**
1) Object가 Detected된 메세지 콘솔에 출력
2) 카메라 중앙으로 배치
3) 각도 계산에 의해 포 정렬
4) 발사 준비 완료 sign이 오면 5초 카운트다운 시작
5) 5초가 지난 이후 발사 버튼 활성화
6) 발사 버튼 클릭 시 남은 포 개수 감소 
![](https://velog.velcdn.com/images/jimeaning/post/eef46d6e-f6d3-477c-afe9-9f9703db4a63/image.png)

**발사 완료 및 시스템 재개** <br>
발사가 완료되면 포를 원상태로 복귀시키고, 카메라를 다시 돌리면서 새로운 타겟을 감지할 준비를 한다.
![](https://velog.velcdn.com/images/jimeaning/post/d564f85f-09b6-4cf2-9adf-9bca705defcd/image.png)

**탄 개수 관리** <br>
준비한 탄이 모두 소진되었을 시에 메세지를 보내 탄을 채워 넣을 수 있도록 한다.![](https://velog.velcdn.com/images/jimeaning/post/a53beb40-8711-4eed-90c1-a648924c6da1/image.png)

### 🚶‍♀️ Video (Client)

[![](https://img.youtube.com/vi/RkoLZZuFiAo/0.jpg)](https://youtu.be/RkoLZZuFiAo?t=0s)

### 🌀 HW Output
**시스템 구동 (표적 감시)**
![](https://velog.velcdn.com/images/jimeaning/post/799fdca0-e9e3-4a24-92ba-6c2e9ac4880c/image.png)

**표적 Detect 및 Classification**
![](https://velog.velcdn.com/images/jimeaning/post/17921886-6c56-48e8-8b1e-2ffc212a6ba6/image.png)

**표적 특성에 맞는 무기 선택 및 포 각도 제어 이후 LED 점화**
![](https://velog.velcdn.com/images/jimeaning/post/54f76940-2c87-4251-82b2-4ab05bf8c902/image.png)

**발사 준비 완료 시 발사 LED 점화**
![](https://velog.velcdn.com/images/jimeaning/post/5d214bd2-173b-4243-90b3-433287df168d/image.png)

### 🌀 Video (HW)
[![](https://img.youtube.com/vi/cgCJSf1lH84/0.jpg)](https://youtu.be/cgCJSf1lH84?t=0s)

## 🚩 개발 과정
![](https://velog.velcdn.com/images/jimeaning/post/1c2fd11a-72f5-4ef5-990e-7952816bc7ae/image.png)

### 프로젝트 주제 선정 및 설계
![](https://velog.velcdn.com/images/jimeaning/post/a430057f-4fff-4551-8b0c-c4637064681d/image.png)

### 데이터 수집 및 전처리
![](https://velog.velcdn.com/images/jimeaning/post/076dcbc3-0cb1-4db9-ae2d-068331da8a1e/image.png)

![](https://velog.velcdn.com/images/jimeaning/post/b2a2617a-9c26-4f4a-8b53-09965d01536c/image.png)
![](https://velog.velcdn.com/images/jimeaning/post/7ba19be9-86c8-4458-af41-615a243bb674/image.png)
- Plane : Plane, Helicopter, Fighter-jet
- Car : Retona, Two-half, Tank
- Human
- Chaos (두 개 이상의 object가 섞여 있는 사진)

총 900장 수집 


### HW 동작 확인, 카메라 깊이 정보 확인
![](https://velog.velcdn.com/images/jimeaning/post/f25036fa-f195-4957-8812-90e635539a87/image.png)
![](https://velog.velcdn.com/images/jimeaning/post/4a53fa6a-bd0f-4638-ad0e-297f91f2e37d/image.png)

### 알고리즘 확인용 샘플 코드 제작
![](https://velog.velcdn.com/images/jimeaning/post/1023e8ac-cbbe-4225-ab13-8f8d7c104378/image.png)

### 코드 상세 작성
![](https://velog.velcdn.com/images/jimeaning/post/200cfe0a-25e4-41c5-931f-e2b8bc14cb61/image.png)

## Github milestone
![](https://velog.velcdn.com/images/jimeaning/post/c06088fe-db90-4ef7-b3b0-afa9dbe8ff85/image.png)


## Clone code

```shell
git clone https://github.com/oz971124/BTS.git
```

## Prerequite

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Steps to build

```shell
cd ~/BTS
./setup.sh
```

## Steps to run

**Follow the order : Server -> User -> RaspberryPi**

**1. for Server**

```shell
cd ~/BTS
source .venv/bin/activate
cd Server
python3 main.py
```

**2. for User**

```shell
cd ~/BTS
source .venv/bin/activate
cd User
python3 main.py
```

**3. for RaspberryPi**

- Camera

```shell
cd ~/BTS/RaspberryPi/build
sudo ./program
```

- HW

```shell
cd ~/BTS
source .venv/bin/activate
cd RaspberryPi
python3 rasp2server.py
```

