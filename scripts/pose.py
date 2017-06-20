#!/usr/bin/env python
from __future__ import print_function
from tf.transformations import euler_from_quaternion
import numpy as np

class Pose(object):
    def __init__(self, x=0, y=0, z=0, yaw=0):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.marker_ids = list()
        self.current_marker_id = None
        self.max_found = False

    def __str__(self):
        return "x: {}    y: {}   z: {}   yaw: {}".format(self.x, self.y, self.z, self.yaw)

    def convert_geometry_transform_to_pose(self, transform, aruco_mapping, aruco_front):
        try:
            euler = euler_from_quaternion((transform.orientation.x,
                                            transform.orientation.y,
                                            transform.orientation.z,
                                            transform.orientation.w
                                            ))
            if aruco_mapping:
                self.z = transform.position.x
                self.x = transform.position.z
                self.y = -transform.position.y
                self.yaw = euler[1]
            elif aruco_front:
                self.x = transform.position.z
                self.y = -transform.position.y
                self.z = transform.position.x
                self.yaw = -euler[1]
            else:
                self.x = transform.position.x
                self.y = transform.position.y
                self.z = transform.position.z
                self.yaw = euler[2]

        except AttributeError:
            euler = euler_from_quaternion((transform.rotation.x,
                                            transform.rotatoion.y,
                                            transform.rotation.z,
                                            transform.rotation.w
                                            ))
            self.x = transform.translation.x
            self.y = transform.translation.y
            self.z = transform.translation.z
            self.yaw = euler[2]
                
            

    def as_waypoints(self):
        return np.around(np.array([self.x, self.y, self.z, self.yaw]), decimals=3)

    def store_marker_ids(self, marker_ids):
       self.marker_ids = marker_ids

    def get_marker_ids(self):
       return self.marker_ids

    def store_current_marker_id(self, current_marker_id):
       self.current_marker_id = current_marker_id

    def get_current_marker_id(self):
       return self.current_marker_id

    def get_max_found(self):
        return self.max_found

    def set_max_found(self, max_found):
        self.max_found = max_found