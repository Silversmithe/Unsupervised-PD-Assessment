"""

    draw static stuff
    push actual matrix on stack (glPushMatrix)
    load identity matrix (initial matrix) (glLoadIdentity)
    use your own matrix and load and set it as the actual matrix
    transform the actual matrix via glRotate / gl....
    save the actual matrix as your own matrix
    draw your object
    pop matrix from stack (glPopMatrix)
    draw rest of the static stuff

"""
from visual.quad import QuadPoly
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

delta = 5.0                     # amount to change rotation
x_rot, y_rot, z_rot = 0,0,0     # initializing orientation
palm = QuadPoly(0.75, 0.75 , 0.25)
point = QuadPoly(0.10, 0.5, 0.10, -0.75/4 - 0.0625, 0.625, 0)
ring = QuadPoly(0.10, 0.5, 0.10, 0.75/8, 0.625, 0)
thumb = QuadPoly(0.10, 0.5, 0.10, -0.75/2 - 0.0625, 0, 0)
# extra fingers
f3 = QuadPoly(0.10, 0.625, 0.10, -0.75/8, 0.690, 0)
f5 = QuadPoly(0.10, 0.375, 0.10, 0.75/4 + 0.0625, 0.565, 0)

def display():
    global palm, point, ring, thumb, f3, f5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    # hand
    # rotation transformation
    glRotate(x_rot, 1, 0, 0)
    glRotate(y_rot, 0, 1, 0)
    glRotate(z_rot, 0, 0, 1)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)

    # palm
    for line in palm.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    # adjust pointer
    for line in point.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    # adjust thumb
    for line in thumb.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    for line in ring.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    for line in f3.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    for line in f5.lines:
        glVertex3f(line[0][0], line[0][1], line[0][2])
        glVertex3f(line[1][0], line[1][1], line[1][2])

    glEnd()
    glPopMatrix()

    glFlush()
    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)

def keyboard(key, x, y):
    global x_rot
    global y_rot
    global delta

    if key == b' ':           # press space key to exit
        sys.exit( )
    elif key == b'w':
        x_rot = x_rot + delta # + x
    elif key == b's':
        x_rot = x_rot - delta # - x
    elif key == b'a':
        y_rot = y_rot + delta # + y
    elif key == b'd':
        y_rot = y_rot - delta # - y

def idle():
    glutPostRedisplay()

if __name__ == '__main__':
    global quadratic

    glutInit()
    quadratic = gluNewQuadric()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow('Basic Cube Hand Model')
    glutReshapeWindow(512, 512)
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

glutMainLoop()
