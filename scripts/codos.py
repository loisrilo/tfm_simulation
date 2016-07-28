import math

# Specific geometry for my delta robot:
e = 130.0  # small triangle side (EE)100
f = 125.0  # support triangle side215
re = 205.0  # upper arm length350
rf = 150.0  # lower arm length250
hf = math.sqrt(0.75*(f**2))
he = math.sqrt(0.75*(e**2))

dtr = math.pi / 180.0  # degrees to radians

# Initial points
A1 = [hf/3, 0, 0]
A2 = [-A1[0]*math.cos(60*dtr), -A1[0]*math.sin(60*dtr), 0]
A3 = [A2[0], -A2[1], 0]


def punto_codo(theta):
    theta *= dtr
    b1 = [A1[0]+rf*math.cos(theta), 0.0, rf*math.sin(theta)]
    return b1

sin120 = math.sin(120*dtr)
cos120 = math.cos(120*dtr)
def rotacion120(ent):
    sal = [0.0, 0.0, 0.0]
    sal[0] = cos120*ent[0]+sin120*ent[1]
    sal[1] = -sin120*ent[0]+cos120*ent[1]
    sal[2] = ent[2]
    return sal


sin240 = math.sin(240*dtr)
cos240 = math.cos(240*dtr)
def rotacion240(ent):
    sal = [0.0, 0.0, 0.0]
    sal[0] = cos240*ent[0]+sin240*ent[1]
    sal[1] = -sin240*ent[0]+cos240*ent[1]
    sal[2] = ent[2]
    return sal


def sumav(v1, v2):
    s = [0.0, 0.0, 0.0]
    s[0] = v1[0] + v2[0]
    s[1] = v1[1] + v2[1]
    s[2] = v1[2] + v2[2]
    return s


vhe1 = [he/3, 0.0, 0.0]
vhe2 = rotacion120(vhe1)
vhe3 = rotacion120(vhe2)
def punto_ee(ee, brazo):
    sal = [0.0, 0.0, 0.0]
    if brazo == 1:
        sal = sumav(ee, vhe1)
    elif brazo == 2:
        sal = sumav(ee, vhe2)
    elif brazo == 3:
        sal = sumav(ee, vhe3)
    return sal


def rotacion_y(ent, ang):
    sal = [0.0, 0.0, 0.0]
    sal[0] = ent[0]*math.cos(ang) - ent[2]*math.sin(ang)
    sal[1] = ent[1]
    sal[2] = -ent[0]*math.sin(ang) + ent[2]*math.cos(ang)
    return sal

def angulos_codo(codo, ee, brazo):
    if brazo == 2:
        codo = rotacion240(codo)
        ee = rotacion240(ee)
    elif brazo == 3:
        codo = rotacion120(codo)
        ee = rotacion120(ee)
    if (codo[0]-ee[0]) != 0:
        ang_a = math.atan((ee[2]-codo[2])/(codo[0]-ee[0]))
    else:
        ang_a = 1.570796326794897
    # prep
    codo = rotacion_y(codo, ang_a)
    ee = rotacion_y(ee, ang_a)
    # calc
    if (codo[0]-ee[0]) != 0:
        ang_b = math.atan((ee[1])/(codo[0]-ee[0]))
    else:
        ang_b = 0
    return [ang_a, ang_b]