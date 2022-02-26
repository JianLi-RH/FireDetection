import subprocess
import tempfile
import base64
import os, shutil
from os import listdir
from os.path import isfile, join
from xxlimited import Null

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response

from FireDetection.fire.models import Interfaces
from FireDetection.fire.utilities import *

# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def checkFireStatus(request):
    try:
        photo = request.FILES.get('photo')
        detect = 'FireDetection/fire/FireAI/detect.py'
        source = 'FireDetection/fire/FireAI/demo/1.png'
        weight = 'FireDetection/fire/FireAI/best.pt'
        # save_dir = f'FireDetection/fire/results'
        save_dir = tempfile.mkdtemp()

        # Clear folder
        for files in os.listdir(save_dir):
            path = os.path.join(save_dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)

        # write picture to local
        with open(f'{save_dir}/{photo.name}', 'wb') as destination:
            destination.write(photo.read())

        # Call yolov5 to check if fired
        script = f"python {detect} --source {save_dir}/{photo.name} --project {save_dir}  {weight}"
        print(script)
        # r = subprocess.call(script, stdout=subprocess.PIPE, shell=True)
        p = subprocess.Popen(['python', detect, '--source', f"{save_dir}/{photo.name}", '--project', save_dir, '--weights', weight], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            bufsize=256*1024*1024)
        print(f"AI验证结果{p}")
        output, errors = p.communicate()
        if p.returncode:
            raise RuntimeError(f"AI验证结果{errors}")
        else:
            # Print stdout from cmd call
            print(output)

        firedPictures = [f for f in listdir(f"{save_dir}/exp") if isfile(join(f"{save_dir}/exp", f))]
        print(firedPictures)
        print(len(firedPictures))

        status, msg = (0, '没有着火点') if len(firedPictures) < 1 else (1, '着火了')

        # Convert the fired picture into base64 string
        base64Str = ''
        if status == 1:
            with open(f'{save_dir}/exp/{photo.name}', 'rb') as img:
                base64Str = str(base64.b64encode(img.read()), encoding='utf-8')

            cameraID = request.data['cameraID']
            print(f"相机编号：{cameraID}")

            url = Interfaces.objects.get_or_create(name='DK识别')
            if url[0].url:
                # 调用接口存盘
                data = {'Base64':base64Str, 'CameraID':cameraID, 'AppId':'', 'AppSecret':''}
                print(f"post to {url[0].url}")
                post(url[0].url, data=data)
            else:
                return Response({'status':'92', "message": "无法找到'DK识别'接口"})

        # response
        return Response({'status': f"{status}", "message": f"{msg}", "fired" : base64Str})
    except Exception as ex:
        return Response({'status':'90', "message": f"验证失败: {ex}"})