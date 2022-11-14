import uvage

camera = uvage.Camera(600, 600)
pyImage = uvage.from_image(300,300,"https://www.python.org/static/img/python-logo@2x.png")
speed = 2

def tick():
    global speed
    camera.clear("black")
    pyImage.x += speed
    if pyImage.x > 400 or pyImage.x < 200:
        speed *= -1
    camera.draw(pyImage)
    camera.display()

uvage.timer_loop(30, tick)