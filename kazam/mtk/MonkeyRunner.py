__author__ = 'Lambert Liu'
import time
import sys
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

#����Ӧ�ð��������Activity��
pakageName = 'com.hujiang.cctalk'
componentName = 'com.hujiang.cctalk/.MainActivity'

#APP����ʱ�ȴ�ʱ��(��)
startTime = 5

#��ȡ������ʱ����
now = time.strftime("%Y-%m-%d-%H-%M-%S")

#python�л�ȡ��ǰ���е��ļ�������
name=sys.argv[0].split("\\")
filename=name[len(name)-1]

#MonkeyRunner�»�ȡ���е��ļ����ڵ�·��
rootpath  = os.path.split(os.path.realpath(sys.argv[0]))[0]

#ָ��λ��
dir = rootpath + "/apk/"
screenPath = rootpath + "/screenShot/"
logpath = rootpath + "/log/"

#��ȡ����APK����
countPak = len(os.listdir(dir))

#�½�һ��Log�ļ�
if not os.path.isdir(logpath):
    os.mkdir(logpath)
log = open( logpath + filename[0:-3] + "-log" +now + ".txt" , 'w')

#��ʼ�����豸
print("Connecting...")
device = MonkeyRunner.waitForConnection()
log.write("�����豸...\n")

#ж��Ӧ��
print('Removing...')
device.removePackage(pakageName)
print ('Remove Successful!')
MonkeyRunner.sleep(2)
log.write("��ʼ��Ӧ�û���...\n")
countOK = 0
countNO = 0

for i in os.listdir(dir):
    print('Installing...<%s>'%i)
    log.write("==========��װӦ��==========\n")
    path = dir + '//' + i
    #��װӦ��
    device.installPackage(path)
    print('Install Successful!')

    #��Ӧ��
    device.startActivity(component=componentName)
    MonkeyRunner.sleep(startTime)
    log.write("����App...\n")

    #��ͼ
    result=device.takeSnapshot()
    print("Take ScreenShot...")

    #�����ͼ
    result.writeToFile(screenPath + i + '.png','png')

    #����ͼƬ�Ƚ�
    resultTrue=MonkeyRunner.loadImageFromFile(screenPath + r'basePic.png')
    print "Pic Comparing..."
    log.write("�Ա�ͼƬ��...\n")
    if(result.sameAs(resultTrue,0.9)):
        print("%s is OK!"%i)
        log.write("�Ƚ�ͨ����--%s--�����ã�\n"%i)
        #ж��Ӧ��
        print('Removing...')
        log.write("��ʼ��Ӧ�û������Ƴ���...\n")
        device.removePackage(pakageName)
        print ('Remove Successful!')
        log.write("==========�Ƴ����==========\n")
        countOK += 1
        MonkeyRunner.sleep(2)
    else:
        print("False!Please check %s!"%i)
        log.write("�Ƚ�ʧ�ܣ����鰲װ��--%s--�Ƿ���ã�\n"%i)
        break

log.write("������ %s ������%d ��ͨ����"%(countPak,countOK))