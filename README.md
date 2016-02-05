# R2Helper ![David](https://img.shields.io/david/strongloop/express.svg) ![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen.svg) ![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
QQR2 (QQ音速) 출석 이벤트 자동 참여 스크립트

## 시스템 요구사항
- UTF-8 인코딩 출력을 지원하는 쉘 (`cmd.exe`의 경우 `chcp65001`명령어 이후 작동 가능)
- Python 3.4 이상 (설치 : https://www.python.org/ 에서 최신 버전을 내려 받으세요)

## 사용 방법
* 쉘에서 다음을 입력하고 출력되는 지침을 따릅니다.
```
git clone https://github.com/k3nuku/R2Helper --recursive
cd R2Helper
cd qqlib
pip install -r requirements.txt
python setup.py build
python setup.py install
cd ..
python r2helper.py
```

## 사용 예 (Example)
###입력
```
python r2helper.py -i 3243322432 -p r2helperzzang -n thisismynick
```

###결과
```
[i] QQ번호 3243322432로 로그인을 시도합니다.
[i] 로그인에 성공하였습니다. (계정 3243322432, 닉네임 k3nuku)
[*] thisismynick 캐릭터의 출석 토큰 정보를 가져옵니다.
[!] 오늘의 출석 체크가 이미 완료된 상태입니다.
[*] 캐릭터 thisismynick에 Thu 접속 보상 받기를 시도합니다.
[!] 19시 접속 보상 작업이 완료되었습니다.
[!] 20시 접속 보상 작업이 완료되었습니다.
[!] 21시 접속 보상 받기를 실패하였습니다. 해당 시간에 접속하지 않았습니다.
[i] 모든 작업이 완료되었습니다. 애플리케이션을 종료합니다.
```

##License
R2Helper is licensed under the MIT License. The terms are as follows :
```
The MIT License (MIT)

Copyright (c) 2016 Dong Kyun Yoo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
