
# 🚀 표적 탐지 미사일 자동화 시스템

![](https://velog.velcdn.com/images/jimeaning/post/607480bd-88ce-44d8-ae55-8583f6038a54/image.png)

**표적을 감지하여 알맞은 미사일 선택 후 올바른 각도와 세기로 격파하는 시스템**이다. <br>
줄어드는 청년 인구에 따른 군 인력 문제를 해결하기 위한 타겟 포착 및 분석 자동화 적 섬멸 시스템

## 🦿 High Level Design

- **Sequence Diagram**

![](https://velog.velcdn.com/images/jimeaning/post/e3ffa80a-ba46-4fc5-9d02-969eba477bf9/image.png)

- **Class Diagram**

![image](https://github.com/jimeaning/BTS/assets/62744644/cdae17cc-fc73-495a-9611-3314cca90495)

- **통신 Sequence**
![image](https://github.com/jimeaning/BTS/assets/62744644/4325ec3f-ddf0-40e1-8881-cabab186c258)


## 🦿 개발 동기 및 필요성
![image](https://github.com/jimeaning/BTS/assets/62744644/ced902e1-4e87-41a3-a3bd-d85c86589b5b)

- 국방에서도 기계화되는 움직임이 늘어나고 있다. 최근 인구 감소로 인해 군 병력 인원이 줄었고, 기술의 발전이 원인이다. 기계화를 통해 CCTV 등 인원을 효율적으로 간소화시킬 수 있으며 사람이 놓친 정보를 기계가 포착하는 등 협업이 가능해진다.
- 자동화 격추 시스템을 통해 출동할 인원이 부족하거나 제약이 있을 때, 통제실에서 감시, 탐지, 결정, 준비, 발사 모든 과정을 수행할 수 있다.
- 감시 및 탐지 과정에는 두 가지 경우가 나올 수 있다.
(1) 표적을 확실히 detect를 했을 때
사람은 기계가 정하는 타이밍에 따라 결정을 내리면 된다.
(2) 표적이 애매하게 detected 되었을 때
완전한 자동화와 부분적 자동화의 문제가 있다. 컴퓨터의 판단과 사람의 개입 중 각각의 효율성과 정확도이 어느정도 되는지 판단되어야 한다. 완전 자동화의 가능성이 궁금해 시작하게 된 프로젝트이다.

## HLD - 시스템 아키텍처
![image](https://github.com/jimeaning/BTS/assets/62744644/fa4de51c-99dd-4ee0-a929-7398ae921d40)

**RaspberryPi**
-   HW 모듈 제어
-   서버와 GUI에서 메시지를 수신 받아 처리
-   서버로 웹캠 프레임 전송
-   GUI로 발사 버튼 활성화 메시지 전송
-   C++, CMake, make 사용

**RaspberryPi - 회로도**
![image](https://github.com/jimeaning/BTS/assets/62744644/9435d382-7699-4fbc-8034-92761cadb0b6)

## Server
![image](https://github.com/jimeaning/BTS/assets/62744644/5153d5be-0e0a-42b9-a036-9ebded0ecc7e)
![image](https://github.com/jimeaning/BTS/assets/62744644/d3bfe7c0-bd66-4328-a5cc-6d6f5160ade8)

### Class Diagram
![image](https://github.com/jimeaning/BTS/assets/62744644/21bdae1d-8937-4390-a6a8-5996c4e5f787)


### Object Detection
![image](https://github.com/jimeaning/BTS/assets/62744644/425d37dd-21c5-40f4-948b-18c33ee8d66e)

### Classification
![image](https://github.com/jimeaning/BTS/assets/62744644/b33947c0-bff2-45a8-8c25-7545692a6be8)

## User
![](https://velog.velcdn.com/images/jimeaning/post/9a70e703-063e-4b44-bd65-ac3c2f61e0d6/image.png)
-   서버로 부터 Inferencing된 이미지 수신
-   HW로부터 동작 메시지 수신
-   HW로 발사 명령 송신

### Class Diagram
![image](https://github.com/jimeaning/BTS/assets/62744644/25bfe350-cc4b-430b-bed1-a6c373b2983b)


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

## Output

* (프로젝트 실행 화면 캡쳐)



## Appendix

* (참고 자료 및 알아두어야할 사항들 기술)
