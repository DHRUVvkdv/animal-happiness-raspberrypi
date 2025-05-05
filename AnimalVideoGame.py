import RPi.GPIO as GPIO
import time
import pygame
import random
import requests
from post_animal_data import post_animal_data


colorList = [
    "red",
    "blue",
    "green",
    "orange",
    "purple",
]  # list of possible color cues that can be given
defaultScreen = (255, 255, 255)

# def postData() {
#   requests.post(url, params=params, headers=headers, json = obj)
# }

GPIO.setmode(GPIO.BCM)  # sets pins to be referred to by pin number

# defines GPIO pins as I/O
button1 = 5  # optimistic button, input pin
button2 = 6  # pessimistic button, input pin
motor = 23  # motor control, output pin
sensor = 21  # animal sensor, output pin

# pin default state (state when pin is not pushed)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin reads low
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin reads low
GPIO.setup(sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin reads low
GPIO.setup(motor, GPIO.OUT)  # output pins


# buttonPress(duration): sets output pin to high once button is pressed,
# leaves pin high the amount of time specified in function call
# param: duration - how long output pin should stay high, how long
# 		motor should run
def buttonPress(duration):
    GPIO.output(motor, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(motor, GPIO.LOW)


def visualCueDisplay(color, screen):
    displayColor = random.choice(color)  # random choose color of cue
    screen.fill(displayColor)  # fill screen with said color
    pygame.display.flip()  # function call to update screen display

    running = True  # flag of display running
    startTime = time.time()

    while running:
        timeElapsed = time.time() - startTime

        if GPIO.input(button1) == GPIO.HIGH:
            screen.fill(defaultScreen)  # fill screen with default color
            pygame.display.flip()  # function call to update screen display
            post_animal_data(cow_id="N/A", response_type="pessimistic")
            buttonPress(5)  # run motor for 5 seconds
            running = False  # set flag to false to stop displaying cue
        elif GPIO.input(button2) == GPIO.HIGH:
            screen.fill(defaultScreen)  # fill screen with default color
            pygame.display.flip()  # function call to update screen display
            post_animal_data(cow_id="N/A", response_type="optimistic")
            buttonPress(15)  # run motor for 15 seconds
            running = False  # stop displaying screen
        elif timeElapsed >= 30:
            screen.fill(defaultScreen)  # fill screen with default color
            pygame.display.flip()  # function call to update screen display
            running = False  # too much time passed, stop showing display


try:
    pygame.init()  # initialize pygame
    pygame.mixer.init()  # initialize sound source

    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN
    )  # set to Fullscreen mode)
    screen.fill(defaultScreen)  # fill screen with default color
    pygame.display.flip()  # function call to update screen display
    sound = pygame.mixer.Sound(
        "/home/animalvideogame/BellSoundCue.wav"
    )  # load audio cue

    startTime = time.time()
    running = True
    while running:
        currTime = time.time() - startTime
        if currTime >= 30:
            playing = sound.play()  # play audio cue
            while playing.get_busy():
                pygame.time.delay(100)
            startTime = time.time()

        if GPIO.input(sensor) == GPIO.HIGH:  # animal detected
            visualCueDisplay(colorList, screen)  # display color cue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
        time.sleep(0.1)  # debounces delay

    pygame.quit()  # deinitialize pygame
    GPIO.cleanup()  # reset pins to default

except KeyboardInterrupt:
    pygame.quit()  # deinitialize pygame
    GPIO.cleanup()  # reset pins to default
