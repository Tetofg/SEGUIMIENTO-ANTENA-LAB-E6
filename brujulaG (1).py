from tkinter import  Canvas, Tk, Frame, LAST, Button, ttk
from math import cos, sin, radians, pi,  atan2, degrees
import time
import board
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel

i2c = board.I2C()  # uses board.SCL and board.SDA
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    return vector_2_degrees(magnet_x, magnet_y)

def get_angle(_sensor):
    accel_x, accel_z, _ = _sensor.acceleration
    return vector_2_degrees(accel_x, accel_z)

ventana = Tk()
ventana.title('Brujula')
ventana.geometry('620x650+290+10')
ventana.config(bg='black')

frame = Frame(ventana, height=600, width = 600, bg='black', relief ='sunken')
frame.grid(columnspan=2,row=0)

canvas = Canvas(frame, bg='black', width=585, height = 585, relief = 'raised', bd =1)
canvas.grid(padx=5, pady =5) 

nivel =0

def progressBar():
    nivel = get_heading(mag)
    elevacion = get_angle(accel)
    canvas.create_rectangle(0,0,75,75, fill="white")
    canvas.create_oval(100,100,500,500, fill="", outline = '', width =5)
    canvas.create_line(300,300,300+150*sin(radians(nivel-8)), 300-150*cos(radians(nivel+8)),
        fill='black', width = 600)
    canvas.create_line(300,300,300+150*sin(radians(nivel+8)), 300-150*cos(radians(nivel+8)),
        fill='black', width = 600)

    canvas.create_line(300,300,300+150*sin(radians(nivel)), 300-150*cos(radians(nivel)),
        fill='deep sky blue', width = 20)


    canvas.create_oval(150,150,450,450,fill='', outline='dark violet', width=6)
    canvas.create_oval(180,180,420,420,fill='gray22',outline='dark violet', width=6)

    texto = int(nivel)
    texto = str(texto)
    texto1 = int(elevacion)
    texto1 = str(texto1)
    canvas.create_text(25,30, text= texto1, font=('Arial', 22,'bold'), fill = 'deep sky blue')    
    canvas.create_text(300,300, text= texto, font=('Arial', 42,'bold'), fill = 'deep sky blue')
    canvas.create_text(300,350, text= 'Brujula', font=('Cambria Math', 22,'bold'), fill = 'white')
    canvas.create_text(300,380, text= 'Digital', font=('Freestyle Script', 25,'bold'), fill = 'orange')
    canvas.create_text(300,100, text= 'N', font=('Freestyle Script', 25,'bold'), fill = 'red')	
    canvas.create_text(170,25, text= 'Elevacion', font=('Freestyle Script', 18,'bold'), fill = 'orange')

style = ttk.Style()
style.configure("Horizontal.TScale", background="black")
Button(ventana, text='Iniciar', bg='green2', width=20, command=progressBar).grid(column=0, row=1, padx=3, pady=5)
ventana.mainloop()


