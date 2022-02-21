# FireDetection

Setup step:
1. git clone https://github.com/JianLi-RH/FireDetection.git
2. git clone https://github.com/JianLi-RH/FireAI.git
3. Run below command to move FireAI/ into FireDetection/FireDetection/fire
    mv FireAI/ FireDetection/FireDetection/fire
4. download best.pt and put it into folder FireDetection/FireDetection/fire/FireAI
5. Build docker image with below command:
    $ docker build --tag fire:latest .


安装步骤：
1. git clone https://github.com/JianLi-RH/FireDetection.git
2. git clone https://github.com/JianLi-RH/FireAI.git
3. 执行以下命令，将FireAI/移动到FireDetection/FireDetection/fire文件夹下
    mv FireAI/ FireDetection/FireDetection/fire
4. 下载 best.pt 并将其放在 FireDetection/FireDetection/fire/FireAI文件夹下
5. Build docker image with below command:
    $ docker build --tag fire:latest .

运行镜像：
docker run --name fire -d -p 8000:8000 fire:latest

接口文档：

1. /fire/check
    作用：检查图片中是否包含起火点
    登录：否
    请求方式：post
    请求参数：
        参数名： photo, 参数类型： 图片
        参数名： cameraID, 参数类型： 文本
    
    返回值：
        状态： status， 0： 没着火， 1： 起火了， 9： 执行异常
        消息： message，如：没有着火点
        起火图片base64码： fired

        举例:
        {
            "status": "0",
            "message": "没有着火点",
            "fired": ""
        }