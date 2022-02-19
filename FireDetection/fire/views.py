import subprocess
import tempfile
import base64
import os, shutil
from os import listdir
from os.path import isfile, join

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response

from FireDetection.fire.serializers import UserSerializer, GroupSerializer

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
        script = f"python {detect} --source {save_dir}/{photo.name} --project {save_dir} --weights {weight}"
        print(script)
        r = subprocess.call(script, shell=True)

        firedPictures = [f for f in listdir(f"{save_dir}/exp") if isfile(join(f"{save_dir}/exp", f))]
        print(firedPictures)
        print(len(firedPictures))

        status, msg = (0, '没有着火点') if len(firedPictures) < 1 else (1, '着火了')

        # Convert the fired picture into base64 string
        base64Str = ''
        if status == 1:
            with open(f'{save_dir}/exp/{photo.name}', 'rb') as img:
                base64Str = base64.b64encode(img.read())

        # response
        return Response({'status': f"{status}", "message": f"{msg}", "fired" : base64Str})
    except KeyError:
        return Response({'status':'9', "message": "验证失败!"})