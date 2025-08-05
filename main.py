from turtle import Screen
import turtle
import time
import random
import pygame

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load sounds
sound_wall = pygame.mixer.Sound("wall.wav")
sound_paddle = pygame.mixer.Sound("paddle.wav")
sound_brick = pygame.mixer.Sound("brick.wav")
sound_lose = pygame.mixer.Sound("lose.wav")
sound_win = pygame.mixer.Sound("win.wav")


screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("breakout")
screen.tracer(0)

# Score and lives
score = 0
lives = 3
difficulty = 1.0  # Use as delay factor

# Draw score/lives
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0    Lives: 3", align="center", font=("Courier", 18, "normal"))

# create paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# create ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 4
ball.dy = -4

# create bricks
bricks = []

colors = ["red", "orange", "yellow", "green", "blue"]

for y in range(250, 150, -20):
    for x in range(-350, 400, 70):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(random.choice(colors))
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(x, y)
        bricks.append(brick)





# create  paddle movement
def go_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 30)

def go_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 30)

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# Update scoreboard
def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}    Lives: {lives}", align="center", font=("Courier", 18, "normal"))


# Reset ball
def reset_ball():
    global difficulty
    ball.goto(0, 0)
    ball.dx = random.choice([-4, 4])
    ball.dy = -4
    time.sleep(1)
    difficulty = 1.0  # Reset difficulty

# runing the game
running = True
while running:
    screen.update()
    time.sleep(0.01 * difficulty)

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall bounce
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1
        sound_wall.play()

    if ball.ycor() > 290:
        ball.dy *= -1
        sound_wall.play()

    # Missed paddle
    if ball.ycor() < -290:
        lives -= 1
        update_scoreboard()
        sound_lose.play()
        if lives == 0:
            pen.goto(0, 0)
            pen.write("Game Over", align="center", font=("Courier", 24, "bold"))
            running = False
        else:
            reset_ball()

    # Paddle bounce
    if (ball.ycor() < -230 and ball.ycor() > -240) and (abs(ball.xcor() - paddle.xcor()) < 60):
        ball.sety(-230)
        ball.dy *= -1
        sound_paddle.play()

    # Brick collision
    for brick in bricks:
        if brick.distance(ball) < 35:
            ball.dy *= -1
            sound_brick.play()
            brick.goto(1000, 1000)
            bricks.remove(brick)
            score += 10
            difficulty *= 0.98
            update_scoreboard()

    # Win condition
    if not bricks:
        pen.goto(0, 0)
        pen.write("You Win!", align="center", font=("Courier", 24, "bold"))
        sound_win.play()
        running = False




# Update scoreboard
def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}    Lives: {lives}", align="center", font=("Courier", 18, "normal"))






screen.mainloop()
screen.exitonclick()


