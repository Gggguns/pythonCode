#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import math

# ãÐÖµ
PER_THRESHOLD = 0.1
OBS_THRESHOLD = 0.1
output_done=False

#扫描障碍物
def lidarCallback(msg):
    global output_done
    if output_done:
         return
    obstacles = []
    refer = 1

    for i in range(3585):
        if 597 <= i <= 2988:  # ºöÂÔÌØ¶¨·¶Î§
            continue

        if msg.ranges[i] < 1:  # ¾àÀëÐ¡ÓÚ1Ã×
            if abs(refer - msg.ranges[i]) >= PER_THRESHOLD:  # ãÐÖµÅÐ¶Ï
                if i < 1192 and abs(refer - msg.ranges[i + 1]) >= PER_THRESHOLD and abs(refer - msg.ranges[i + 2]) >= PER_THRESHOLD:
                    distance = (msg.ranges[i] + msg.ranges[i + 1] + msg.ranges[i + 2]) / 3.0
                    angle = (msg.angle_min + msg.angle_increment * i) * (180 / math.pi)
                    obstacles.append((distance, angle))  # Ö±½Ó´æ´¢Ôª×é

                if i > 2488:
                    if i + 1 < 3585 and abs(refer - msg.ranges[i + 1]) >= PER_THRESHOLD:
                        if i+2 < 3585 and abs(refer - msg.ranges[i + 2]) >= PER_THRESHOLD:
                            distance = (msg.ranges[i] + msg.ranges[i + 1] + msg.ranges[i + 2]) / 3.0
                            angle = (msg.angle_min + msg.angle_increment * i) * (180 / math.pi)
                            obstacles.append((distance, angle))  # Ö±½Ó´æ´¢Ôª×é

        obs_start = msg.ranges[i]
        t = i
        while t < 3585:
            if abs(obs_start - msg.ranges[t]) >= OBS_THRESHOLD:
                break
            t += 1
        i = t - 1

    if obstacles:
        # Ê¹ÓÃ min() ÕÒµ½¾àÀë×îÐ¡µÄÕÏ°­Îï
        closest_obstacle = min(obstacles, key=lambda obs: obs[0])  # »ñÈ¡¾àÀë×îÐ¡µÄÔª×é
        rospy.loginfo(f"Distance: {closest_obstacle[0]:.2f} meters, Angle: {closest_obstacle[1]:.2f} degrees")
        output_done=True
    else:
        rospy.loginfo("No significant obstacles detected.")

#障碍物检测
def  obstacleDetection():
    #rospy.init_node('radar_scanning_node')  
    # ¶©ÔÄ¼¤¹âÀ×´ïÊý¾Ý
    rospy.Subscriber("/scan", LaserScan, lidarCallback)
    while not rospy.is_shutdown():
        if output_done:
            rospy.signal_shutdown("Output completed, shutting down node.")





