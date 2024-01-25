import math
import random

# ADD SPHYNX DOC FORMAT


# Representation for the final object
class physical_object:
    def __init__(self, angle, distance, width):
        self.angle = angle
        self.distace = distance
        self.width = width

    def angle():
        return self.angle

    def distance():
        return self.distance

    def __str__(self):
        return (
            "{\n\tangle: "
            + str(self.angle)
            + ",\n\tdistance: "
            + str(self.distace)
            + ",\n\twidth: "
            + str(self.width)
            + "\n}"
        )


# Generate sample lidar data with a few objects
class lidar_sample:
    def __init__(self):
        self.data = [float("inf")] * 760
        for i in range(0, 50):
            self.data[i] = random.uniform(1.0, 1.1)
        for i in range(80, 114):
            self.data[i] = random.uniform(3.2, 3.3)
        for i in range(530, 620):
            self.data[i] = random.uniform(1.5, 1.6)
        for i in range(700, len(self.data)):
            self.data[i] = random.uniform(1.0, 1.1)


# Class for doing the data processing
class lidar_data_processor:
    # A representation of a single index of the lidar data
    class lidar_point:
        def __init__(self, idx, dist):
            self.idx = idx
            self.dist = dist

        # Allow comparrison: Compares length
        def __eq__(self, other):
            return self.dist == other.dist

        def __lt__(self, other):
            return self.dist < other.dist

        # Printable in object notation
        def __repr__(self):
            return "POINT: {idx: " + str(self.idx) + ", dist: " + str(self.dist) + "}"

    def __init__(self, depth_threshold, width_threshold):
        self.data = lidar_sample().data
        print("------------lidar-data-------------")
        print(self.data)
        print("-------------all-point-distances------------")
        self.depth_threshold = depth_threshold
        self.width_threshold = width_threshold
        self.tolerance = depth_threshold
        self.objects = []  # 2-D array of lidar_point objects
        self.physical_objects = []

    # Populate objects by searching through points
    def collect_object_pointsets(self, min_num, max_num):
        # Store a set of the previously created points. (lidar_point)
        last_points = []
        # Store a set of lidar_point objects
        current_object = []
        # Loop through the length of the lidar data array
        for index in range(len(self.data)):
            # Get the distance of current point
            point = self.data[index]
            # Compare to previous points
            if len(last_points) > 0:
                # If this point's distance is within the threshold of the previous point's distance
                if self.compare(last_points[0], point, self.depth_threshold):
                    # Add a new lidar_point to the current object.
                    current_object.append(self.lidar_point(index, point))
                    # If we've reached the end of the lidar data set...
                    if index >= len(self.data) - 1:
                        # Add the current object array to objects
                        self.objects.append(current_object)
                        # Reset the current object
                        current_object = []
                # If not within the threshold but the current object has points
                elif len(current_object) > 0:
                    # Make sure the object isn't a bunch of inf values
                    if min(current_object).dist != float("inf"):
                        # Get the angle at the middle of the object
                        current_obj_angle = (360 / len(self.data)) * (
                            current_object[int(len(current_object) / 2)].idx
                        )
                        self.objects.append(current_object)

                    # -->                # <-- Need to get min distance and total width (deg) -->

                    # obj = physical_object(current_obj_angle, min(current_object).dist, (360/len(self.data)) * len(current_object))
                    # self.physical_objects.append(obj)
                    current_object = []

            else:
                current_object.append(self.lidar_point(index, point))
            # Add every point to the front of the previous points set.
            last_points.insert(0, point)

    # Take the points collected and interperet them into physical object representations.
    # Problem: lidar_point is getting injected as width.
    def process_points_to_objects(self):
        print("OBJECTS________")
        print(len(self.objects))
        if len(self.objects) > 1:
            print(self.objects[0][len(self.objects[0]) - 1])
            if self.compare(
                self.objects[0][len(self.objects[0]) - 1].dist,
                self.objects[len(self.objects) - 1][0].dist,
                self.depth_threshold,
            ):
                self.combine_abstract_objects(
                    self.objects[0], self.objects[len(self.objects) - 1]
                )
                del self.objects[0]
                del self.objects[len(self.objects) - 1]
        for obj in self.objects:
            angle = (360 / len(self.data)) * (obj[int(len(obj) / 2)].idx)
            dist = min(obj).dist
            width = (360 / len(self.data)) * len(obj)
            self.physical_objects.append(physical_object(angle, dist, width))

    # Compare two points and return true if their difference is within the supplied tolerance.
    def compare(self, a, b, tolerance):
        dif = abs(a - b)
        return dif <= tolerance

    # Combine two objects that are connected by a point
    def combine_abstract_objects(self, obj1, obj2):
        total_len = len(obj1) + len(obj2)
        mid = int(total_len / 2)
        if mid < len(obj1):
            mid_obj = obj1
        else:
            mid_obj = obj2
            mid = mid - len(obj1)

        obj_angle = (360 / len(self.data)) * (mid_obj[mid].idx)
        mins = [min(obj1), min(obj2)]
        min_dist = min(mins).dist
        width = (360 / len(self.data)) * total_len
        self.physical_objects.append(physical_object(obj_angle, min_dist, width))


ldp = lidar_data_processor(0.15, 0)
ldp.collect_object_pointsets(0, 0)
ldp.process_points_to_objects()
print("PRINTING OBJECTS...")
for obj in ldp.physical_objects:
    print()
    print()
    print("NEXT OBJ...")
    print(obj)
