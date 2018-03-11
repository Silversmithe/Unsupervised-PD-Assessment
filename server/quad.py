"""
quad.py

Alexander S. Adranly

defines a cube object that can be rendered by OpenGL
"""

class QuadPoly(object):

    def __init__(self, length, width, height, x=0.0, y=0.0, z=0.0):
        """
        define oneself
        """
        self.length = length
        self.width = width
        self.height = height
        self.origin = {'x': x, 'y': y, 'z': z}
        self.rotation = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.coordinates = [] # a list of pairs (a line) of each array

        #####################
        # BUILD COORDINATES #
        #####################
        v1 = [self.origin['x'] - (self.length/2),
              self.origin['y'] + (self.width/2),
              self.origin['z'] + (self.height/2) ]

        v2 = [self.origin['x'] - (self.length/2),
              self.origin['y'] + (self.width/2),
              self.origin['z'] - (self.height/2) ]

        v3 = [self.origin['x'] + (self.length/2),
              self.origin['y'] + (self.width/2),
              self.origin['z'] + (self.height/2) ]

        v4 = [self.origin['x'] + (self.length/2),
              self.origin['y'] + (self.width/2),
              self.origin['z'] - (self.height/2) ]

        v5 = [self.origin['x'] + (self.length/2),
              self.origin['y'] - (self.width/2),
              self.origin['z'] + (self.height/2) ]

        v6 = [self.origin['x'] + (self.length/2),
              self.origin['y'] - (self.width/2),
              self.origin['z'] - (self.height/2) ]

        v7 = [self.origin['x'] - (self.length/2),
              self.origin['y'] - (self.width/2),
              self.origin['z'] + (self.height/2) ]

        v8 = [self.origin['x'] - (self.length/2),
              self.origin['y'] - (self.width/2),
              self.origin['z'] - (self.height/2) ]

        ###############
        # BUILD LINES #
        ###############
        self.lines = [
            # face 1
            [v1,v2], [v3,v4], [v1,v3], [v2,v4],
            # face 2
            [v7,v8], [v5,v6], [v7,v5], [v8,v6],
            # connectors
            [v7,v1], [v8,v2], [v5,v3], [v6,v4]
        ]
