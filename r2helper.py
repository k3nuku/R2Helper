import qqlib
import random
import json
import sys
import getopt
import datetime

# 광동 = 209
# 두번째도장
# http://apps.game.qq.com/r2/a20130601today/SignSecond.php?callback=jQuery1520694240930955857_1454589589803&_=1454590089057

class R2Helper(object):
    URL_SIGN_DAY = 'http://apps.game.qq.com/cgi-bin/r2/a20130601today/SignDay.cgi?areaid=209&roleid=%s&type=2&rid=%f'
    URL_RECEIVE_REWARD = 'http://apps.game.qq.com/cgi-bin/r2/a20130601today/GetOnlinePackage.cgi?areaId=209&roleId=%d&timeNum=%s&dayType=%s&rid=%f'
    URL_CHECK_ROLE = 'http://apps.game.qq.com/cgi-bin/r2/CheckRole/CheckRole.cgi?ssn=209&r=%f'
    URL_SIGN_DAY_ACTIVE = 'http://apps.game.qq.com/cgi-bin/r2/a20130601today/SignDay.cgi?areaid=209&roleid=%s&type=1&rid=%s'

    def print_usage(self):
        print("R2Helper 1.0 by Sokdak, Code with Python3.4. 코드는 MIT License를 따릅니다.\n사용 방법 : python3 r2helper.py -i <QQ 번호> -p <비밀번호> -n <19~21시 접속 보상 받을 캐릭터 닉네임>")

    def print_arg_error(self):
        print("* 아이디나 비밀번호가 입력되지 않았습니다. 올바르게 입력하였는지 확인하세요.\n비밀번호에 공백이 포함되어 있을 경우 쌍따옴표로 묶어 주세요.\n")
        self.print_usage()

    def qq_login(self, id, pw):
        qq = qqlib.QQ(id, pw)

        try:
            qq.login()
        except qqlib.LogInError:
            return None

        return qq

    def validate(self, argv):
        if argv.__len__() == 0:
            self.print_usage()
            return False
        elif argv.__len__() < 3:
            self.print_arg_error()
            return False

        try:
            opts, args = getopt.getopt(argv, "i:p:n:", ["identify=", "password=", "nickname="])
        except getopt.GetoptError:
            self.print_arg_error()
            return False

        for opt, arg in opts:
            if opt in ("-i", "--identify"):
                self.id = int(arg)
            elif opt in ("-p", "--password"):
                self.pw = arg
            elif opt in ("-n", "--nickname"):
                self.nickname = arg

        if self.id == None or self.pw == None or self.id == '' or self.pw == '':
            self.print_arg_error()
            return False

        return True

    def do_sign(self, role_id):
        a = self.qq.session.request(method='get', url=R2Helper.URL_SIGN_DAY % (role_id, random.random()))
        return a.content

    def receive_reward(self, role_id, time_type, day_type):
        a = self.qq.session.request(method='get', url=R2Helper.URL_RECEIVE_REWARD % (role_id, time_type, day_type, random.random()))
        return a.content

    @staticmethod
    def __main__(self, argv):
        self.id = None
        self.pw = None
        self.nickname = None
        self.role_id = None

        if self.validate(argv) == False:
            return -1

        print('[i] QQ번호 %d로 로그인을 시도합니다.' % self.id)
        self.qq = self.qq_login(self.id, self.pw)

        if self.qq is None:
            print('[!] 로그인에 실패하였습니다. 아이디와 비밀번호를 확인해 주세요.')
            return -1
        else:
            print('[i] 로그인에 성공하였습니다. (계정 %d, 닉네임 %s)' % (self.qq.user, self.qq.nick))

        bq_result = self.qq.session.request(method='get', url=R2Helper.URL_CHECK_ROLE % random.random())

        b = str(bq_result.content.decode('gb2312')).replace('\n', '')
        d = json.loads(b[b.index('{'):b.index('}') + 1])

        for z in d['list']:
            if z[0] == 'charac_no':
                continue

            if self.nickname is not None:
                if self.nickname == z[2]:
                    self.role_id = int(z[0])

            print("[*] %s 캐릭터의 출석 토큰 정보를 가져옵니다." % z[2])

            cq_result = self.qq.session.request(method='get', url=R2Helper.URL_SIGN_DAY_ACTIVE % (z[0], random.random()))
            e = cq_result.content.decode('gb2312').replace('\n', '')
            f = json.loads(e[e.index('{'):e.index('}') + 1])

            ret = int(f['iRet'])

            if ret != -1:
                acts = int(f['iActs'])

                if acts >= 30:
                    print("[i] 활동 점수 : %d, 출석 체크 가능 점수입니다. 출석을 시도합니다." % acts)
                    res = self.do_sign(z[0])
                else:
                    print("[!] 활동 점수 : %d, 점수가 부족하여 출석 체크 불가합니다." % acts)
            else:
                print('[!] 오늘의 출석 체크가 이미 완료된 상태입니다.')
                break

        if self.role_id is not None:
            print('[*] 캐릭터 %s에 %s 접속 보상 받기를 시도합니다.' % (self.nickname, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%a")))
            weekday = datetime.datetime.today().weekday()

            for i in range(19, 22):
                if weekday == 6 or weekday == 0: # Monday or Sunday
                    result = self.receive_reward(self.role_id, i, 1)
                else: # Weekday
                    result = self.receive_reward(self.role_id, i, 0)

                if result is None:
                    print('[!] %d시 접속 보상 받기를 실패하였습니다. 네트워크 상 오류가 발생했습니다.' % i)
                    break

                t = str(result.decode('gb2312')).replace('\n', '')
                v = json.loads(t[t.index('{'):t.index('}') + 1])

                if v['iRet'] == '0':
                    print('[i] %d시 접속 보상 작업이 완료되었습니다.' % i)
                else:
                    print('[!] %d시 접속 보상 받기를 실패하였습니다. 해당 시간에 접속하지 않았습니다.' % i)
        else:
            if self.nickname is not None:
                print('[!] %d 계정에 해당 닉네임이 존재하지 않습니다. 정확하게 입력하였는지 확인하세요.' % self.qq.user)
            else:
                print('[!] 19~21시 접속 보상을 받기 위한 닉네임을 입력하지 않아 접속 보상받기를 진행할 수 없습니다.')

        print('[i] 모든 작업이 완료되었습니다. 애플리케이션을 종료합니다.')
        return 0

if __name__ == '__main__':
    r2helper = R2Helper()
    R2Helper.__main__(r2helper, sys.argv[1:])
