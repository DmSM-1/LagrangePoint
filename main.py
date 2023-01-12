import graphics as gr
import math

SIZE_X = 700
SIZE_Y = 700
CENTER_X = SIZE_X/2
CENTER_Y = SIZE_Y/2
RADIUS = 300
GM = 1
GME = GM/100
FirstV = math.sqrt(GM/RADIUS)
num = 200


class Star:
    x = SIZE_X / 2
    y = SIZE_Y / 2
    plot = gr.Circle(gr.Point(float(x), float(y)), 20)
    plot.setFill('yellow')

class Planet:
    radius = RADIUS
    x = CENTER_X+RADIUS
    y = CENTER_Y
    Vfirst = math.sqrt(GM/radius)
    Vx = 0
    Vy = -Vfirst
    plot = gr.Circle(gr.Point(x, y), 10)
    plot.setFill('blue')
    LagRad = radius*(GME/3/GM)**(1/3)

    L1Rad = radius - LagRad
    L1x = L1Rad
    L1y = y
    L1 = gr.Circle(gr.Point(x-LagRad, y), 3)
    L1.setFill('violet')

    L2Rad = radius + LagRad
    L2x = L2Rad
    L2y = y
    L2 = gr.Circle(gr.Point(x+LagRad, y), 3)
    L2.setFill('violet')

    L3Rad = -radius
    L3x = L2Rad
    L3y = y
    L3 = gr.Circle(gr.Point(x - 2*radius, y), 3)
    L3.setFill('violet')

class OrbitalObj:
    radius = RADIUS
    x = CENTER_X + RADIUS
    y = CENTER_Y
    Vfirst = FirstV
    Vx = 0
    Vy = -Vfirst


window = gr.GraphWin("Lagrange",float(SIZE_X), float(SIZE_Y))
window.setBackground("black")

obj = []
objP = []

for i in range(num):
    obj.append(OrbitalObj())
    obj[i].radius = (2.5 * RADIUS/num*(i+1) - RADIUS)+0.001
    obj[i].y = CENTER_X + obj[i].radius * math.sin(2*math.pi / num * i * 0)
    obj[i].x = CENTER_Y + obj[i].radius * math.cos(2*math.pi / num * i * 0)
    obj[i].Vfirst = FirstV/RADIUS*obj[i].radius
    obj[i].Vy = -obj[i].Vfirst * math.cos(2 * math.pi / num * i*0)
    obj[i].Vx = obj[i].Vfirst * math.sin(2 * math.pi / num * i*0)
    objP.append(gr.Circle(gr.Point(obj[i].x, obj[i].y), 2))
    objP[i].setFill('red')
    objP[i].draw(window)
objP[0].setFill('black')


Sun = Star
Sun.plot.draw(window)

Terra = Planet()
Terra.plot.draw(window)
Terra.L1.draw(window)
Terra.L2.draw(window)
Terra.L3.draw(window)


def move_Terra():
    Vx, Vy = Terra.Vx, Terra.Vy
    print()
    Terra.plot.move(Terra.Vx, Terra.Vy)
    Terra.L1.move(Terra.Vx * Terra.L1Rad/Terra.radius, Terra.Vy* Terra.L1Rad/Terra.radius)
    Terra.L2.move(Terra.Vx * Terra.L2Rad/Terra.radius, Terra.Vy* Terra.L2Rad/Terra.radius)
    Terra.L3.move(-Terra.Vx, -Terra.Vy)
    r15 = ((Terra.x - Sun.x) ** 2 + (Terra.y - Sun.y) ** 2)**1.5
    Terra.Vx += ((GM * (Sun.x - Terra.x)) / r15)
    Terra.Vy += ((GM * (Sun.y - Terra.y)) / r15)
    Terra.x += Vx
    Terra.y += Vy


def move_obj(i):
    Vx, Vy = obj[i].Vx, obj[i].Vy
    objP[i].move(obj[i].Vx, obj[i].Vy)
    r15 = ((obj[i].x - Sun.x) ** 2 + (obj[i].y - Sun.y) ** 2)**1.5
    rE15 = ((obj[i].x - Terra.x) ** 2 + (obj[i].y - Terra.y) ** 2) ** 1.5
    obj[i].Vx += ((GM * (Sun.x - obj[i].x)) / r15)+((GME * (Terra.x - obj[i].x)) / rE15)
    obj[i].Vy += ((GM * (Sun.y - obj[i].y)) / r15)+((GME * (Terra.y - obj[i].y)) / rE15)
    obj[i].x += Vx
    obj[i].y += Vy

    if r15<10 or (obj[i].Vx**2+obj[i].Vy**2)>50*FirstV**2:
        objP[i].setFill('black')

while(True):
    move_Terra()
    for i in range(len(obj)):
        move_obj(i)
