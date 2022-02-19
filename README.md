# FireDetection

Setup step:
1. download/clone git@github.com:JianLi-RH/FireDetection.git
2. download/clone git@github.com:JianLi-RH/FireAI.git
3. Run below command to move FireAI/ into FireDetection/FireDetection/fire
    mv FireAI/ FireDetection/FireDetection/fire
4. download best.pt and put it into folder FireDetection/FireDetection/fire/FireAI
5. Build docker image with below command:
    $ docker build --tag django_todo:latest .


安装步骤：
1. download/clone git@github.com:JianLi-RH/FireDetection.git
2. download/clone git@github.com:JianLi-RH/FireAI.git
3. 执行一下命令，将FireAI/移动到FireDetection/FireDetection/fire文件夹下
    mv FireAI/ FireDetection/FireDetection/fire
4. 下载 best.pt 并将其放在 FireDetection/FireDetection/fire/FireAI文件夹下
5. Build docker image with below command:
    $ docker build --tag django_todo:latest .