import math
import random

class Blob:
    def __init__(self, pos=(0,0), r=0):
        self.pos = pos
        self.r = r

        self.col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))


        
        self.next = None
        self.prev = None

    def get_bounding_box(self):
        return ((self.pos[0]-self.r, self.pos[1]-self.r),(self.pos[0]+self.r, self.pos[1]+self.r))
    
    def get_bounding_box_int(self):
        return ((int(self.pos[0]-self.r), int(self.pos[1]-self.r)),(int(self.pos[0]+self.r), int(self.pos[1]+self.r)))

    def __str__(self):
        return str(self.pos[0]) + ", "+str(self.pos[1]) +" - "+str(self.r)
    
    def dist(self, b):
        dx = self.pos[0] - b.pos[0]
        dy = self.pos[1] - b.pos[1]
        return math.sqrt(dx*dx+dy*dy)
    
    def pos_int(self):
        return (int(self.pos[0]), int(self.pos[1]))


def create_blob_from_keypoint(keypoint):
    return Blob((keypoint.pt[0],keypoint.pt[1]), keypoint.size/2)

def find_change(blobs_old, blobs_new, params):

    def compare(a):
        return a[2]

    changes = []

    maxDist = 1000000

    dists = []
    for old in blobs_old:
        for new in blobs_new:
            bruh = old.dist(new)
            if(bruh <= 30):
                dists.append((old, new, bruh))
    
    dists.sort(key=compare)
    
    needed = len(blobs_old)
    have = 0
    i = 0
    while(have < needed and i < len(dists)):
        old, new, distance = dists[i]
        i+=1
        if(old.next == None and new.prev == None):
            old.next = new
            new.prev = old
            new.col = old.col
            have+=1
        
    

    