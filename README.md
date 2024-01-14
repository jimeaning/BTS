# Project BTS

* 표적 탐지 미사일 자동화 시스템
표적을 감지하여 알맞은 미사일 선택 후 올바른 각도와 세기로 격파하는 시스템  
줄어드는 청년 인구에 따른 군 인력 문제를 해결하기 위한 초소 자동화 시스템

## High Level Design

- **Sequence Diagram**

![](./Documents/sequence_diagram_v3.png)

- **Class Diagram**

![](./Documents/class_diagram_v3.png)


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
