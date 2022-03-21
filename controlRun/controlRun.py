import Arm_Lib
import time
import math
import rospy 
from std_msgs.msg import Float32MultiArray
import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server



###############################################
# setup our server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# setup our own namespace, not really necessary but should as spec
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# get Objects node, this is where we should put our nodes
objects = server.get_objects_node()

# populating our address space
myobj = objects.add_object(idx, "ROS")

myvarContr = myobj.add_variable(idx,"Control", 0, ua.VariantType.Boolean)
myvarConfirm=myobj.add_variable(idx,"Confirm", 0, ua.VariantType.Boolean)

myvarSentX = myobj.add_variable(idx, "SentX", 6.7)
myvarSentY = myobj.add_variable(idx, "SentY", 6.7)
myvarSentZ = myobj.add_variable(idx, "SentZ", 6.7)
myvarSentState = myobj.add_variable(idx, "SentState", 1,ua.VariantType.Boolean)

myvarGotX = myobj.add_variable(idx, "GotX", 6.7)
myvarGotY = myobj.add_variable(idx, "GotY",  6.7)
myvarGotZ = myobj.add_variable(idx, "GotZ", 6.7)
myvarGotState = myobj.add_variable(idx, "GotState", 1,ua.VariantType.Boolean)

myvarContr.set_writable()    # Set MyVariable to be writable by clients
myvarGotX.set_writable() 
myvarGotY.set_writable() 
myvarGotZ.set_writable() 
myvarGotState.set_writable() 

# starting!
server.start()
######################################################



######################################################
#robot initialize
Arm = Arm_Lib.Arm_Device()
time.sleep(.1)
joints_0 = [90, 135, 20, 25, 90, 30]#1
joints_length=[11,8.5,18]
now_state=False
aim_pose=[]

Arm.Arm_serial_servo_write6_array(joints_0, 1500)
print("ok")
######################################################    
    

    
######################################################
#angle transformation func
def D2R(x):
    return x/180*math.pi

def R2D(x):
    return x/math.pi*180
######################################################



######################################################
#robot movement func
def positionSet(aimPose):
    print("aimPose")
    print(aimPose)
    x=aimPose[0];
    y=aimPose[1];
    z=aimPose[2];
    angleFinal=aimPose[3]
    #      
    #     y  .
    #          .
    #x  ...........    
    #          .
    #          .
    if x==0:
        angle1=90
    elif y==0:
        if x>0:
            angle1=180
        elif x<0:
            angle1=0
    else:
        angle1=math.atan(x/y)#
        angle1=R2D(angle1)+90
    m=(x**2+y**2)**0.5
    c=(x**2+y**2+z**2)**0.5
    n=(m**2+(z-11)**2)**0.5
    if angleFinal<0.5:#
        angle5=30
    else:angle5=150

    if n>26.5:
       angle2=math.acos(m/c)
       angle2=R2D(angle2)
       c_rest=c-joints_length[0]
       if c_rest<joints_length[1]+joints_length[2]:
           angle_3=math.acos((joints_length[1]**2+c_rest**2-joints_length[2]**2)/2/joints_length[1]/c_rest)
           angle_3=R2D(angle_3)
           angle3=angle_3+90
           angle_4=math.acos((joints_length[1]**2+joints_length[2]**2-c_rest**2)/2/joints_length[1]/joints_length[2])
           angle_4=R2D(angle_4)
           angle4=angle_4-90
           joints_next=[angle1,angle2,angle3,angle4,90,angle5]
           Arm.Arm_serial_servo_write6_array(joints_next, 1500)
           print(angle1,angle2,angle3,angle4,angle5)
           print("n>26.5")
       else:
           angle3=90
           angle4=90
           joints_next=[angle1,angle2,angle3,angle4,90,angle5]
           Arm.Arm_serial_servo_write6_array(joints_next, 1500)
           print(angle1,angle2,angle3,angle4,angle5)
           print("c>46.5")
    else: 
        if n<8.5:
           n=8.5
        angle_3=math.acos((joints_length[0]**2+n**2-c**2)/(2*joints_length[0]*n))
        angle_3=R2D(angle_3)
        angle4=math.acos((joints_length[1]**2+joints_length[2]**2-n**2)/(2*joints_length[1]*joints_length[2]))#
        angle4=R2D(angle4)-90
        angle_4=math.acos((joints_length[1]**2+n**2-joints_length[2]**2)/(2*joints_length[1]*n))
        angle_4=R2D(angle_4)
        angle3=angle_4+angle_3-90
        angle2=90
        joints_next=[angle1,angle2,angle3,angle4,90,angle5]
        Arm.Arm_serial_servo_write6_array(joints_next, 1500)
        print(angle1,angle2,angle3,angle4,angle5)
     


def dis(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def z_calculate(propotion):
    if(propotion>=1 or propotion<=0):
        return 0
    elif not now_state:
        _prop=math.sqrt(math.fabs(0.6-propotion)/(1.0-propotion))
        z=20+_prop*20/(1.0-_prop)
        return z
    elif now_state:
        _prop=math.sqrt(math.fabs(0.6-propotion)/math.fabs(1.0-propotion))
        z=20+_prop*20/(1.0-_prop)
        return z

def state_judge(points_list):
    change=0
    for i in range(1,4):
        if points_list[i*4+1][1]<points_list[i*4+3][1]:
            change=change+1
    if change>=2:
        return True
    else: return False


    
def movement(points_list,nowstate):#,aim_posi):
    global aim_pose
    if aim_pose:
        _aim_pose=[aim_pose[0],aim_pose[1],aim_pose[2],aim_pose[3]]
    aim_pose=[]
    temp_state=state_judge(points_list)
    if not temp_state:
    #if temp_state==nowstate and not temp_state:
           #dis_prop=dis(points_list[0],points_list[8]) #
           dis_prop=dis(points_list[0],points_list[2])  #
           tang_indextip_length=14.0
           tang_indexmcp_length=5.0
           #real_dis= tang_indextip_length/dis_prop #
           real_dis= tang_indexmcp_length/dis_prop
           z_cor=z_calculate(dis_prop)
           final_cor=((-0.5+points_list[0][0])*real_dis,z_cor/2.5,(1-points_list[0][1])*real_dis)
           aim_pose.append((-0.5+points_list[0][0])*real_dis)
           aim_pose.append(z_cor/5.0)
           aim_pose.append((-0.5+points_list[0][1])*real_dis)
           aim_pose.append(nowstate)
           print(aim_pose)
    elif temp_state:
    #elif temp_state==nowstate and temp_state:
          dis_prop=dis(points_list[0],points_list[2])
          tang_indexmcp_length=5.0
          real_dis= tang_indexmcp_length/dis_prop
          z_cor=z_calculate(dis_prop)
          final_cor=((-0.5+points_list[0][0])*real_dis,z_cor/2.5,(1-points_list[0][1])*real_dis)
          #aim_pos.position=((-0.5+points_list[0][0])*real_dis,z_cor/5.0,(-0.5+points_list[0][1])*real_dis)
          #aim_pos.orientation=(nowstate,0,0)
          aim_pose.append((-0.5+points_list[0][0])*real_dis)
          aim_pose.append(z_cor/5.0)
          aim_pose.append((-0.5+points_list[0][1])*real_dis)
          aim_pose.append(nowstate)
          print(aim_pose)
    elif temp_state!=nowstate:
          aim_pose=[_aim_pose[0],_aim_pose[0],_aim_pose[0],temp_state]
          print("statechange")
          time.sleep(1)
    return temp_state
#####################################################################################################    



#####################################################################################################
#callback func and whole control
def info_handle(PoseArray=[]):
    global aim_pose
    #if no control
    if not myvarContr.get_value():
        print("no control_got")
        #so handle the opencvInfo
        global now_state
        poseArray=[]
        now_state=False
        for i in range (0,21):
            poseArray.append([PoseArray.data[3*i],PoseArray.data[3*i+1],PoseArray.data[3*i+2]])
        now_state=movement(poseArray,now_state)
        #and then to the screen
        myvarSentX.set_value(aim_pose[0])
        print(myvarSentX.get_value())
        print(aim_pose[0])
        myvarSentY.set_value(aim_pose[1])
        myvarSentZ.set_value(aim_pose[2])
        myvarSentState.set_value(aim_pose[3])
        
    #if control
    elif myvarContr.get_value():
        aim_pose=[]
        print("control_got")
        #then got the pose from screen
        aim_pose.append(myvarGotX.get_value())
        aim_pose.append(myvarGotY.get_value())
        aim_pose.append(myvarGotZ.get_value())
        aim_pose.append(myvarGotState.get_value())
        print(myvarGotX.get_value())
        print(myvarGotY.get_value())
        print(myvarGotZ.get_value())
        print(myvarGotState.get_value())        
    #finally according to the aim_pose to the pose
    print("movement_got")
    positionSet(aim_pose)
    
#####################################################################################################
    
    

#####################################################################################################
#ros func
def listener():
 
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    if not myvarContr.get_value():
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("pose",Float32MultiArray, info_handle)
        
    else:
        info_handle()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
####################################################################################################
    
    
   
####################################################################################################
#start and end
listener()
#close connection, remove subcsriptions, etc
server.stop()
####################################################################################################








