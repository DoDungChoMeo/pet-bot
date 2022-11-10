import turtle
import random

t = turtle.Turtle()
s = turtle.Screen()

s.bgcolor('white')
t.pencolor('pink')
t.shape('turtle')
t.hideturtle()

t.pensize(3)
t.speed(50)
t.penup()
t.goto(0, 200)
t.pendown()

a = 0
b = 0
while True:
  t.forward(a)
  t.right(b)
  a+=5
  b+=1
  if b == 210:
    break

turtle.done()
