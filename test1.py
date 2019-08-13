import dvrkArm
import time
import math
import rospy

MILLION = 10**6

ps = dvrkArm.dvrkArm('/PSM1')
pos_des = [0.0, 0.0, -0.13]  # Position (m)
rot_des = [0, 0, 0]  # Euler angle ZYX (or roll-pitch-yaw)
jaw_des = [0]
ps.set_pose(pos_des, rot_des, 'deg')

cnt = 0.0
interval_ms = 10
amp = 0.04
period = 5.0
rate = rospy.Rate(1000.0 / interval_ms)
t_sleep = 0.5
while not rospy.is_shutdown():
    try:
        p = amp*math.sin(2*math.pi*cnt/period)
        ps.set_pose([0.0, p, -0.13], [0.0, 0.0, 0.0], 'deg', True)
        cnt += 1000.0 / MILLION * interval_ms
        rate.sleep()
    except rospy.ROSInterruptException:
        pass