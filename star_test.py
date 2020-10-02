
import plotly.graph_objects as go
import numpy as np
import random
import math
from scipy.spatial.distance import euclidean as distance
from operator import itemgetter as get 
import json

layout = go.Layout( 
    width=1000,
    height=1000,
    xaxis={"range": [-2, 102]},
    yaxis={"range": [-2, 102]},
)

fig = go.Figure(layout=layout)

def generate_star_points(_star):
    r_inner = _star["r_inner"]
    r_outer = _star["r_outer"]
    phi_0 = _star["phi_0"]
    x = _star["x"]
    y = _star["y"]

    x_arr = []
    y_arr = []
    step = 72

    for i in range(6):
        rads = np.deg2rad(step * i + phi_0)

        x_arr.append(-r_outer*np.sin(rads) + x)
        y_arr.append(r_outer*np.cos(rads) + y)

        rads = np.deg2rad(step * i + 36 + phi_0)

        x_arr.append(-r_inner*np.sin(rads) + x)
        y_arr.append(r_inner*np.cos(rads) + y)

    return (x_arr, y_arr)

def generate_accurate_star_points(_star):
    (x_arr, y_arr) = generate_star_points(_star)

    accuracy = 4
    x_new_arr = []
    y_new_arr = []
    zip_points = zip(x_arr[:-1], x_arr[1:], 
                     y_arr[:-1], y_arr[1:])

    for (x, x_next, y, y_next) in zip_points:
        dx = (x_next - x) / accuracy
        dy = (y_next - y) / accuracy

        for i in range(accuracy):
            x_new_arr.append(x + i * dx)
            y_new_arr.append(y + i * dy)

    return (x_new_arr,y_new_arr)

def hard_check(_star1, _star2):
    p1arr = generate_accurate_star_points(_star1)
    p2arr = generate_accurate_star_points(_star2)

    dr = ((p1arr[0][1]-p1arr[0][0])**2+
          (p2arr[1][1]-p2arr[1][0])**2)**0.5
    
    for p1 in zip(p1arr[0],p1arr[1]):
        for p2 in zip(p2arr[0],p2arr[1]):
            if distance(p1,p2) < dr:
                return True

    return False

def is_stars_intersect(_star1,_star2):
    r_dist = _star1["r_inner"] + _star2["r_outer"] 
    center_dist = distance(get("x", "y")(_star1), 
                           get("x", "y")(_star2))

    print("R_DIST: ")
    print(r_dist)
    print("CENTER_DIST: ")
    print(center_dist)
    if (center_dist < r_dist):
        return True
    elif (center_dist < _star1["r_outer"]*2):
        print("Stars are too close for additional check")
        return hard_check(_star1, _star2)
    else:
        return False

def get_star_scatter(_star):
    (x_arr, y_arr) = generate_star_points(_star)
    return go.Scatter(
        x=x_arr,
        y=y_arr
        )

def get_accurate_star_scatter(_star):
    (x_arr_new, y_arr_new) = generate_accurate_star_points(_star)
    return go.Scatter(
        x=x_arr_new,
        y=y_arr_new
    )

stars = []
star_count = 3
r_inner = 3
r_outer = 10
x_max = 20
y_max = 20

layout = go.Layout( 
    width=1000,
    height=1000,
    xaxis={"range": [-r_outer, x_max+r_outer]},
    yaxis={"range": [-r_outer, y_max+r_outer]},
)

fig = go.Figure(layout=layout)


# for i in range(star_count):
#     stars.append(
#         {
#             "phi_0": random.randint(0, 180),
#             "r_inner": r_inner,
#             "r_outer": r_outer,
#             "x": random.randint(0, x_max),
#             "y": random.randint(0, y_max)
#         }
#     )

stars = [
    {"phi_0": 78, "r_inner": 3, "r_outer": 10, "x": 19, "y": 17},
    {"phi_0": 169, "r_inner": 3, "r_outer": 10, "x": 10, "y": 4}
]

[print(json.dumps(star)) for star in stars]

s_intersect = {}
for s1 in stars:
    s_intersect_list = []

    for s2 in stars:
        if s1 != s2 and is_stars_intersect(s1, s2):
                s_intersect_list.append(s2)

    s_intersect[json.dumps(s1)] = s_intersect_list

print(s_intersect)


keys = list(s_intersect.keys())
random.shuffle(keys)
keys = set(keys)

final_points = []
while keys:
    k = keys.pop()
    final_points.append(k)

    for each in s_intersect[k]:
        s_str = json.dumps(each)
        if keys and s_str in keys: keys.remove(json.dumps(each))

for each in final_points:
    star_dict = json.loads(each)
    fig.add_trace(get_accurate_star_scatter(star_dict))

fig.show()