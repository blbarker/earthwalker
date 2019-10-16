"""
Try to find the behavior of the problem of walking due N a distance b,
then due W a distance b, then due N a distance b, and end up at the
exact same starting point
"""
import math
import time

# a is the starting point of the walk, defined as the distance from the
#   north pole (i.e. length of the arc).  a is also the angle of that arc
# from the north pole in radians  (we assume radius=1).  Basically 
# latitude measured from the north pole
# b is the length of the arc from point a, as well as the circumference
# of the circle created while walking west.
#
radius_of_earth_miles = 3958.8
arc_of_earth_miles = radius_of_earth_miles * math.pi


def circumference(a, r=1):
    """The circumference as a function of a"""
    # a is the angle from the north pole, so the sin of a will be the
    # radius of the circle we walk going west.  Circ 2*pi*r
    x = r * math.sin(a)
    return 2 * math.pi * x


def test_circumference():
    a = 0
    while a <= math.pi:
        print("a=%3.9f, x=%3.9f" % (a, circumference(a)))
        a += 0.2


def get_lat_str(a):
    """Gets the angle from the north pole in familiar degrees latitude"""
    lat =  90 - (180/math.pi)*a
    if lat > 0:
        return "%3.5f degrees N" % lat
    if lat < 0:
        return "%3.5f degrees S" % -lat
    return "Equator!"


def a_to_b(a, r=1):
    """Computes the b for a given a.  If specified, r is used in printing"""
    start = time.time()
    circ_x = circumference(a)
    increment = 0.1
    b = 0
    x = 0 
    delta = circ_x - b
    while abs(delta) >= 0.000001:
        x = math.sin(a+b)
        circ_x = circumference(a + b)
        #print("b=[%2.9f] --> x=%2.9f" % (b, x))
        delta = circ_x - b
        if delta > 0:
            b += increment
        if delta < 0:
            b -= increment
            increment = increment / 10
            b += increment
    stop = time.time()

    print("a=%2.5f (%s) --> b=%2.5f to %s (%2.12frads) "
          "(x=%2.5f, circ_x=%2.5f, total distance=%2.5f)"
          "(c-x=%2.5f)"
          % (a*r,
             get_lat_str(a),
             b*r, 
             get_lat_str(a+b),
             a+b,
             x*r,
             circ_x*r,
             (b+circ_x)*r,
             (math.pi - a - b - x)*r))
    #print("(tooks %5.4f seconds)" % (stop - start))
    return b

def sweep_a():
    a = 0
    while a < math.pi:
        a_to_b(a, r=radius_of_earth_miles)
        a += 0.1


def find_top():
    """
    Appproach the limit of the northern-most circle for the west walk,
    i.e. the smallest a+b
    """
    a = 0.00001
    while a > 0:
        b=a_to_b(a, r=radius_of_earth_miles)
        a -= 0.0000001
    return b


def find_bottom():
    """Is there a bottom limit?  No, it approaches the south pole"""
    a = math.pi - 0.0001
    while a < math.pi:
        b=a_to_b(a, r=radius_of_earth_miles)
        a += 0.000001
    return b

      
def hillsboro():
    hillsboro_lat = 45.5
    a = (90-hillsboro_lat) * math.pi/180  # radians, from north pole
    b = a_to_b(a)
    end_lat = get_lat_str(a + b)
    print("Starting in Hillsboro at %s (%6.3fmi from north pole), walk south "
          "for %6.3f miles to %s (%6.3f miles from south pole) "
          "(a=%2.9f --> b=%2.9f)"
          % (get_lat_str(a),
             a*radius_of_earth_miles,
             b*radius_of_earth_miles,
             end_lat,
             (math.pi - b - a)*radius_of_earth_miles,
             a, b))

if __name__ == "__main__":
    #er = radius_of_earth_miles
    #circ_eq = circumference(math.pi/2)
    #circ_45n = circumference(math.pi/4)
    #circ_45s = circumference(3*math.pi/4)
    #print ("circ_eq  in miles=%3.3f" % (circ_eq * er))
    #print ("circ_45n in miles=%3.3f" % (circ_45n * er))
    #print ("circ_45s in miles=%3.3f" % (circ_45s * er))
    #go()
    #super_go()
    #hillsboro()
    #print "Final answer=%3.9f" % go()

    #test_circumference()
    #a_to_b(1)
    #sweep_a()
    find_top()  # looks like about 64.57254 degrees S (2.6978rads)
    hillsboro()
    #find_bottom()  The limit is the south pole

