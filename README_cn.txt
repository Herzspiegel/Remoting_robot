###
仓库中的文件除了README之外，
controlRun文件夹里存放的是机械臂的控制程序
js文件是前端网页的控制窗口
###

==============================================
操作步骤说明：

1、使用WinSCP将Github上下载的最新Docker_GettingStarted-FW_202X.Y
以及仓库中的tar.gz的镜像包，移入到PLCNext的用户目录下
URL：https://github.com/PLCnext/Docker_GettingStarted

2、按照Github仓库里文档的执行步骤安装balena-engine
详情参见Hub里的README.md

3、安装完毕后输入balena-engine检查是否安装成功
如果发现daemon守护进程未启动，
通过命令行将balena-engine-daemon程序启动之后
关闭窗口，新建shell就会解决

4、在root的环境下将镜像压缩包解压后，
删除镜像压缩包并使用balena-engine load命令
将从官网仓库中下载的ros-kinetic镜像输入到本地镜像库中
        balena-engine load -i ros_kinetic.tar

##    外部PC制作 ros_kinetic.tar.gz：
        docker pull ros:kinetic
        docker images
        docker save -o ros_kinetic.tar ros:kinetic
        tar -zcvf ros_kinetic.tar.gz ros_kinetic.tar

5、按照README.md将项目环境的配置搭建完毕

6、容器中输入命令roslaunch rosbridge_server rosbridge_websocket.launch

7、在PC上将网页窗口置于前端开启，
Yahboom上电之后启动python程序接收话题消息
接收话题消息请按F12查看控制台输出的{data:Array}

8、在摄像头前移动手势
机械臂会跟随手部动作进行移动和抓取

9、启动显示屏，按下显示屏上的AUTO按钮
将机械臂的运动从跟随手部移动的自动模式调至键入坐标的手动模式
再次按下切换回自动模式

=================================================
