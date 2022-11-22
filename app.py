"""
Dino Game was developed by Nadreha Yelizaveta and inspired by Google's 'Dinosaur Game'.
The essence is to overcome obstacles (cacti, vultures) with a character (dinosaur).
"""

from ursina import *
from ursina import Ursina, curve, application
import random as r

app = Ursina()


### Setting up the window
window.title = 'Dino Game'
window.color = color.white
window.fullscreen = True
window.fps_counter.enabled = False
camera.orthographic = True
camera.fov = 9


### Music connection
audio_list = ['lp-lost-on-you-original.mp3', "Rag'n'BoneMan-Human.mp3", "Lorde-Royals.mp3"]
# when the program starts - different music
audio = Audio(sound_file_name=r.choice(audio_list), autoplay=False)
audio_hit = Audio('assets_beep.wav', loop=False, autoplay=False)


### Creating of text prompts
label = Text(f'Points: {0}', scale=1.3, position=(.3,.4), color=color.black, font='VeraMono.ttf')
label_info = Text('click ENTER to pause', scale=1, position=(-.8,.4), color=color.black33, font='VeraMono.ttf')
label_tip = Text('Try to press the space bar twice :)', scale=1.5, position=(-.4,-.2), color=color.white, font='VeraMono.ttf', visible=False)


### This function is triggered by pressing the button
def click_b():
    audio.resume()
    window.color = color.white
    b.visible = False
    dino.texture = 'dino_1.png'
    label_tip.visible = False
    label.color = color.black
    application.resume()

# Creating a play button
b = Button(icon='play-button.png', scale=.2, position=(0,0), visible=False, disabled=True, on_click=click_b)

# This function is triggered by pressing the 'Enter' button during the game
def click_enter():
    audio.pause()
    window.color = color.black
    b.visible = True
    application.pause()
    label.color = color.white
    label_tip.visible = True


### Creating a ground
ground1 = Entity(model='quad', texture='ground.png', scale=(50,0.3,1), z=1, collider='box')
ground2 = duplicate(ground1, x=50)
pair = [ground1, ground2]

# storing obstacles for further display
cactuses = []
birds = []
points = 0


class Barrier(Entity):

    # the cycle of creating new obstacles
    def newItem(self):
        global points
        delay_ = 2
        # start generating vultures from 100 points
        if self.name == 'bird' and points > 100:
            new = duplicate(self, x=20 + r.randint(0,5), y=r.randint(1,4))
            birds.append(new)
            delay_ = 1.5
        elif self.name == 'cacti':
            new = duplicate(self, x=12 + r.randint(0,5))
            cactuses.append(new)
            if points > 50: delay_ = 1.5
            elif points > 100:  delay_ = 0.5
            elif points > 150:  delay_ = 0.2
        invoke(self.newItem, delay=delay_)
    
    # motion of objects
    def update(self):
        global a, points
        for ground in pair:
            ground.x -= a
            if ground.x < -35:
                ground.x += 100
        for c in cactuses:
            c.x -= a
        for i in birds:
            i.x -= a*1.3

cacti = Barrier(name='cacti', model='quad', texture='cacti.png', x = 15, collider ='box', origin_y=-.3)
bird = Barrier(name='bird', model='quad', texture='vulture-bird-shape.png', collider ='box', x = 15, y=3, scale=0.5)


### Character settings
class Player(Entity):
    # object control
    def input(self, key):
        if key == 'space':
            self.texture = 'dino_1.png'
            self.animate('y', value=2, duration=.2, curve= curve.out_sine)
            self.animate('y', value=0, duration=.4, delay=0.4, curve = curve.in_sine)
    
    # object collision with an obstacle
    def update(self):
        if self.intersects().hit:
            self.texture = 'dino_2.png'
            audio_hit.play()
            reset()

dino = Player(model='quad', collider='box', origin_y=-.4, x=-5, texture='dino_1.png')


### Speed adjustment
def update():
    global points
    points += 0.1
    label.text = f'Points: {round(points)}'
    global a
    if points > 150 : a = 0.01
    else: a = time.dt * 0.7


### Pause/play settings
def input(key):
    if mouse.left:
        b.disabled = True
    elif key == 'enter':
        b.disabled = False
        click_enter()


### Game restart: zeroing points and removing obstacles to their new generation
def reset():
    global cactuses, birds, points
    points = 0
    time.dt = 0
    for c in cactuses:
        destroy(c)
    for i in birds:
        destroy(i)
    cactuses.clear()
    birds.clear()
    b.disabled = False
    click_enter()


### Launching the process of creating obstacles and more
def main ():
    audio.play()
    cacti.newItem()
    bird.newItem()


if __name__ == '__main__':
    main()
    app.run()
