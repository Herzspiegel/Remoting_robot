# **1. Project Introduction**

We used the underlying technical framework of PLCNext from Phoenix. Based on this technology, we implemented the balina-engine (Docker) container software on the PLC and imported the official ROS image in the cloud repository. Ros is used to establish mutual communication between different nodes in the industrial LAN. Complete the exploration of the technical application of gesture recognition technology in the industrial field.


# **2. Project Equipment**



​	The following equipment was prepared for this project:

- Controller - AXC F 3152 - 1069208 ([PHOENIX CONTACT | Controller - AXC F 3152 - 1069208](https://www.phoenixcontact.com/online/portal/us?uri=pxc-oc-itemdetail:pid=1069208&library=usen&tab=1))

- Yahboom DOFBOT Robotic Arm ([Yahboom DOFBOT AI Vision Robotic Arm with ROS Python programming for R](https://category.yahboom.net/collections/r-robotics-arm/products/dofbot-pi))

- Three or four CAT5E or CAT6 Ethernet network cables

- PC，with an RJ45 Ethernet interface and a camera

![AXC 3152](https://dam-mdc.phoenixcontact.com/rendition/156443151564/d8b2399820928046a0bfdad66783c48b/-FJPG-B408)

# **3. Running Project**


## Step 1. Set up the project environment

- The initialized PLCNext platform can use the Ethernet port of the PC for **SSH login**, and the login password is the initial password printed on the PLC.

  > Account: admin; 
  > Passwd: \*\*\*\*\*\*\*\*



- We need to log in to **the PLC's Web configuration page** in the browser at the same time, enter the IP address corresponding to the PLC in the browser (different Ethernet interfaces correspond to different IP addresses), and follow the steps to enter the above account and password to **enter the management panel**.

  > Example: 192.168.1.10 (/1.20/1.30)



- At this time, you need to **configure the ~/.bashrc** file inside the Linux operating system, and then **configure the corresponding firewall port in the Web operation panel**. Open the rules for port input and output of process communication for ros nodes in the firewall.

  > open a new shell, input:

  ```shell
  sudo vim ~/.bashrc
  ```

  > then print i to INSERT:

  ```shell
  source /opt/ros/kinetic/setup.bash
  export ROS_MASTER_URI=http://192.168.1.10:11311
  export ROS_HOSTNAME=192.168.1.10
  ```

  > or directly input in CLI:(when the PLC can't use apt to get vim packet in cloud-Hub)

  ```shell
  sudo echo 'source /opt/ros/kinetic/setup.bash' >> ~/.bashrc && sudo echo 'export ROS_MASTER_URI=http://192.168.1.10:11311' >> ~/.bashrc && sudo echo 'export ROS_HOSTNAME=192.168.1.10' >> ~/.bashrc
  ```

  

- Then perform similar operations on **the ~/.bashrc file in the Raspberry Pi** to ensure that the topic can be received correctly in the communication set up by ROS.

  > here change the 'ROS_HOSTNAME=the static ip address of the Raspberry Pi (192.168.1.*)'

  





## Step 2 Run the project

- Before the release of this version of the project, 
  we had taken this project to participate in the 2021 Phoenix China Innovative Application Competition and won the first prize, 
  when we used a PLC control chip to calculate our palm coordinates. 

![](https://www.demir-int.com/media/image/9f/42/dc/phoenix-contact-logo-approved.png)


- However, due to its lack of computing capability, 
  **the real-time tracking effect** of the robotic arm after the industrial camera collects the data was not as good as we thought 
  (after which **Phoenix launched a dedicated TPU device for calculating images for this defect**, and interested friends can go to [Phoenix's official website](https://www.phoenixcontact.com/online/portal/pc) for more detailed information)
  and the action of the robotic arm had **a high time delay**



- After that, we considered ignoring the computing capability of the PLC first, 
  and **transferred all the operations on the gesture coordinate points to the cloud server provided by mediaippe**, 
  which got **a good low-latency effect**


![mediapipe](https://google.github.io/mediapipe/images/mobile/hand_landmarks.png)



- We used a web program written in **javascript** to replace the original industrial camera's collection of gesture data. 
  In the robotic arm part, we use a relatively simple **python** program for data reception and control of the robotic arm

  ```shell
  python3 controlRun.py
  ```

  

- Admittedly, for an industrial network, **the practice of connecting devices to the Internet is extremely dangerous**. 
  But what we want to achieve is how to combine machines with the rapidly developing image recognition technology in the context of **Industry 4.0** to complete some relatively complex work.



- For more detailed information, please see **README .txt**

> **Note:** 

In the Yahboom robot arm used in the Raspberry Pi development board pre-installed **Ubuntu 20.04LTS** operating system, 
after power-on boot will execute a command similar to roscore to open the rosmaster and some other required processes, 
here we just use the drive of the robot arm to complete the final control work, 
remember to **use the kill command to close the rosmaster process after power-up**, 
Make sure **there is only one rosmaster in the LAN** managing topic messages!