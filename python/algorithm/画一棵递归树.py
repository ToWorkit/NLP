# https://facert.gitbooks.io/python-data-structure-cn/4.%E9%80%92%E5%BD%92/4.7.%E4%BB%8B%E7%BB%8D%EF%BC%9A%E5%8F%AF%E8%A7%86%E5%8C%96%E9%80%92%E5%BD%92/
'''
import turtle

myTurtle = turtle.Turtle()
myWin = turtle.Screen()

def drawSpiral(myTurtle, lineLen):
  if lineLen > 0:
    myTurtle.forward(lineLen)
    myTurtle.right(90)
    drawSpiral(myTurtle, lineLen - 5)

drawSpiral(myTurtle, 100)
myWin.exitionclikc()
'''
import turtle

def tree(branchLen,t):
    if branchLen > 5:
        t.forward(branchLen)
        t.right(20)
        tree(branchLen-15,t)
        t.left(40)
        tree(branchLen-15,t)
        t.right(20)
        t.backward(branchLen)

def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("green")
    tree(75,t)
    myWin.exitonclick()

main()
