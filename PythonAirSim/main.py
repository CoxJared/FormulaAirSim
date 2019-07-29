import sys
sys.path.insert(0 ,'./AirSim/car')
import setup_path 
import airsim

import sys
import math
import time
import argparse
import pprint
import numpy

# Makes the drone fly and get Lidar data
class AirSimParser:

    def __init__(self, log_en=False):

        # connect to the AirSim simulator
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        # self.client.enableApiControl(True)
        # self.car_controls = airsim.CarControls()
        self.log_en = log_en
        

    def startup(self):
        state = self.client.getCarState()
        s = pprint.pformat(state)

        if (self.log_en):
            self.f = open("log.txt", "w+")

        print("Start recording in 3 seconds")
    
    # def car_data_thread(self):
    #     for i in range(100)::
    #         car_speed = self.client.getCarState()
    #         if self.log_en:
    #             self.f.write("\tSpeed %d Gear %d", car_data.speed, car_data.gear)

    #         # Collision State
    #         collision_info = self.client.simGetCollisionInfo()

    #         if collision_info.has_collided and self.log_en:
    #             self.f.write("COLLISION: Pos = %d Normal = %d Impact Pt = %d Name = %d ObjectID = %d", collision_info.position, collision_info.normal, collision_info.impact_point, collision_info.object_name, collision_info.object_id)

    #         time.sleep(0.5)

    def execute(self):

        # for i in range(3):
        
        for i in range(10):
            # car_speed = self.client.getCarState()
            car_data = self.client.getCarState()
            if self.log_en:
                self.f.write("\tTime = %f Speed %d Gear %d\n" % ( i, car_data.speed, car_data.gear))

            # Collision State
            collision_info = self.client.simGetCollisionInfo()

            if collision_info.has_collided and self.log_en:
                self.f.write("COLLISION at pos %s, normal %s, impact pt %s, penetration %f, name %s, obj id %d\n" % (
                    pprint.pformat(collision_info.position), 
                    pprint.pformat(collision_info.normal), 
                    pprint.pformat(collision_info.impact_point), 
                    collision_info.penetration_depth, collision_info.object_name, collision_info.object_id))

            # Lidar Info
            if (i%3 == 0): #Every 3 seconds
                lidarData = self.client.getLidarData()
                if (len(lidarData.point_cloud) < 3):
                    print("\tNo points received from Lidar data")
                else:
                    points = self.parse_lidarData(lidarData)
                    print("Reading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(points)))
                    print("\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
                    print("\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
                    
                    if (self.log_en):
                        self.f.write("Reading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(points)))
                        self.f.write("\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
                        self.f.write("\tlidar orientation: %s\n" % (pprint.pformat(lidarData.pose.orientation)))
                    
            time.sleep(1)
            # time.sleep(5)

    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def log_lidar(self, points):
        # TODO
        print("not yet implemented")

    def stop(self):

        # airsim.wait_key('Press any key to reset to original state')
        print("Shutting down now")

        self.client.reset()

        self.client.enableApiControl(False)

        if (self.log_en):
            self.f.close()
        print("Done!\n")

# main
if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    # arg_parser = argparse.ArgumentParser("Lidar.py makes car move and gets Lidar data")
    # arg_parser.add_argument('-save-to-disk', type=bool, help="save Lidar data to disk", default=False)
    # args = arg_parser.parse_args(args)   



    test = AirSimParser(True)
    test.startup()
    try:
        test.execute()
    finally:
        test.stop()
    # lidarTest = LidarTest()
    # try:
    #     lidarTest.execute()
    # finally:
    #     lidarTest.stop()
