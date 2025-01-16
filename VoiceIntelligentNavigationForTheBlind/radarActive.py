import roslaunch
import rospy
import time

def _activatedtRadar():
   
    radar_launch_file = "/home/nano/rplidar_ws/src/rplidar_ros/launch/view_rplidar_s2.launch"
 
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    
    launch = roslaunch.parent.ROSLaunchParent(uuid, [radar_launch_file])

    print("Starting radar...")
    launch.start() 
    
    time.sleep(5)
   
    print("Radar nodes are running.")
    return launch

#启动雷达
def activatedRadar():

    rospy.init_node('radar_running_node', anonymous=True)

    radar_launch = _activatedtRadar()

    rospy.spin()



    
