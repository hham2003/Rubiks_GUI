'''
This file contains the GUI class for rubix_cube that provides visualization and user interaction

Author: Henry Ham

Version: 2022.04.25
'''

from cross_solver_try2 import Cross_Solver
from rubix_cube import Rubiks_Cube
from tkinter import *
import random

class Cube_Interface:
    ''' This class represents a GUI for interacting with a Rubik's Cube puzzle
        Model and functionality of the cube are handled in a separate class '''
    
    def __init__(self, cube = Rubiks_Cube()):
        ''' Initializes the GUI as a window by displaying the state of the cube
            and providing buttons to turn or scramble the cube '''
        
        self.cube = cube
        
        self.root = Tk()
        self.root.title('AntiSledgeCubing Interactive Model')
        self.root.geometry('600x600')
        
        self.canvas = Canvas(self.root, width = 300, height = 400)
        self.canvas.place(x = 300, y = 300, anchor = CENTER)
        
        self.create_buttons()
        
        self.hint_canvas = Canvas(self.root, width = 200, height = 50)
        self.hint_canvas.place(x = 300, y = 560, anchor = CENTER)
        
        self.display_cube()
        
    def new_scramble(self):
        ''' Resets the cube to solved then scrambles it
            with a generated scramble '''
        
        self.cube.reset()
        self.scramble_cube(self.generate_scramble())
        
        
    def scramble_to_str(self, scramble):
        ''' Takes a scramble as a list, converts it into a
            string, and returns that string
            Parameters:
                scramble - list to convert '''
        
        result = ''
        count = 1
        for move in scramble:
            result += move + '  '
            if count == 14:
                result += '\n'
            count += 1
        
        result.strip()
        
        return result
        
    def create_buttons(self):
        ''' Create buttons for moving each face of the cube or scrambling it and
            place them in the window '''
                
        R_button = Button(self.root, text = 'R', command = lambda: self.scramble_cube('R'), width = 3, height = 2).place(x = 0, y = 50)
        Rp_button = Button(self.root, text = "R'", command = lambda: self.scramble_cube("R'"), width = 3, height = 2).place(x = 50, y = 50)
        L_button = Button(self.root, text = 'L', command = lambda: self.scramble_cube('L'), width = 3, height = 2).place(x = 0, y = 100)
        Lp_button = Button(self.root, text = "L'", command = lambda: self.scramble_cube("L'"), width = 3, height = 2).place(x = 50, y = 100)
        F_button = Button(self.root, text = 'F', command = lambda: self.scramble_cube('F'), width = 3, height = 2).place(x = 0, y = 150)
        Fp_button = Button(self.root, text = "F'", command = lambda: self.scramble_cube("F'"), width = 3, height = 2).place(x = 50, y = 150)
        B_button = Button(self.root, text = 'B', command = lambda: self.scramble_cube('B'), width = 3, height = 2).place(x = 0, y = 200)
        Bp_button = Button(self.root, text = "B'", command = lambda: self.scramble_cube("B'"), width = 3, height = 2).place(x = 50, y = 200)
        U_button = Button(self.root, text = 'U', command = lambda: self.scramble_cube('U'), width = 3, height = 2).place(x = 0, y = 250)
        Up_button = Button(self.root, text = "U'", command = lambda: self.scramble_cube("U'"), width = 3, height = 2).place(x = 50, y = 250)
        D_button = Button(self.root, text = 'D', command = lambda: self.scramble_cube('D'), width = 3, height = 2).place(x = 0, y = 300)
        Dp_button = Button(self.root, text = "D'", command = lambda: self.scramble_cube("D'"), width = 3, height = 2).place(x = 50, y = 300)
        M_button = Button(self.root, text = 'M', command = lambda: self.scramble_cube('M'), width = 3, height = 2).place(x = 0, y = 350)
        Mp_button = Button(self.root, text = "M'", command = lambda: self.scramble_cube("M'"), width = 3, height = 2).place(x = 50, y = 350)
        S_button = Button(self.root, text = 'S', command = lambda: self.scramble_cube('S'), width = 3, height = 2).place(x = 0, y = 400)
        Sp_button = Button(self.root, text = "S'", command = lambda: self.scramble_cube("S'"), width = 3, height = 2).place(x = 50, y = 400)
        E_button = Button(self.root, text = 'E', command = lambda: self.scramble_cube('E'), width = 3, height = 2).place(x = 0, y = 450)
        Ep_button = Button(self.root, text = "E'", command = lambda: self.scramble_cube("E'"), width = 3, height = 2).place(x = 50, y = 450)
        x_button = Button(self.root, text = 'x', command = lambda: self.scramble_cube('x'), width = 3, height = 2).place(x = 500, y = 300)
        xp_button = Button(self.root, text = "x'", command = lambda: self.scramble_cube("x'"), width = 3, height = 2).place(x = 550, y = 300)
        y_button = Button(self.root, text = 'y', command = lambda: self.scramble_cube('y'), width = 3, height = 2).place(x = 500, y = 350)
        yp_button = Button(self.root, text = "y'", command = lambda: self.scramble_cube("y'"), width = 3, height = 2).place(x = 550, y = 350)
        z_button = Button(self.root, text = 'z', command = lambda: self.scramble_cube('z'), width = 3, height = 2).place(x = 500, y = 400)
        zp_button = Button(self.root, text = "z'", command = lambda: self.scramble_cube("z'"), width = 3, height = 2).place(x = 550, y = 400)
        hint_button = Button(self.root, text = 'HINT', command = self.get_hint, width = 4, height = 1).place(x = 300, y = 520, anchor = CENTER)
        new_scramble_button = Button(self.root, text = 'New Scramble', command = self.new_scramble).place(x = 300, y = 60, anchor = N)
        solve_cross_button = Button(self.root, text = 'Solve 1 cross-edge', command = self.solve_cross_edge).place(x = 400, y = 50)
        
    def solve_cross_edge(self):
        ''' Create a Cross_Solver object to solve one edge on the bottom-layer cross '''
        
        cross_solver = Cross_Solver(self.cube)
        cross_solver.insert_edge()
        moves = cross_solver.cross_moves
        self.cube.scramble(moves)
        self.canvas.delete('all')
        self.display_cube()
        
    
    def get_hint(self):
        ''' Post the most relevant hint on the window '''
        
        self.hint_canvas.delete('all')
        self.hint_canvas.create_text(100, 25, text = self.cube.get_hint(), anchor = CENTER)
        
    def generate_scramble(self):
        ''' Generates a random sequence of 20 moves and return it
            as a list
            Returns: generated list '''
        
        moves_list = ["R", "R'", "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2", "U", "U'", "U2", "D", "D'", "D2"]
        
        
        scramble = [moves_list[random.randrange(len(moves_list))] for i in range(20)]
        
        no_repeats = False
        while no_repeats == False:
            repeats = False
            prev = -1
            for move in scramble:
                temp = move
                if prev != -1:
                    if move[0] == prev[0]:
                        scramble[scramble.index(move)] = moves_list[random.randrange(len(moves_list))]
                        repeats = True
                prev = temp
            if repeats == False:
                no_repeats = True
        
        return scramble
        
        
    def display_cube(self):
        ''' Displays the current state of the cube on
            the canvas by drawing all faces '''
        
        self.create_face(self.cube.B, 103, 3, rotation = 2)
        self.create_face(self.cube.U, 103, 103)
        self.create_face(self.cube.L, 3, 103, rotation = 1)
        self.create_face(self.cube.R, 203, 103, rotation = 3)
        self.create_face(self.cube.F, 103, 203)
        self.create_face(self.cube.D, 103, 303)
        
    def create_face(self, face, x1, y1, rotation = 0):
        ''' Draws the given face of the cube as 9 connected
            and properly colored squares
            Parameters:
                face - Specified face taken from cube
                x1 - x value of the first square of the face
                y1 - y value of the first square of the face
                rotation - number of 90° clockwise rotations to
                    correctly orient the given face in the display'''
        
        colors_dict = {0:'white', 1:'green', 2:'red', 3:'blue', 4:'orange', 5:'yellow', -1:'black'}
        
        for i in range(rotation):
            self.cube.move(self.cube.get_face(face))
        rot_face = self.cube.copy_face(face)
        for i in range(rotation):
            self.cube.move(self.cube.get_face(face) + "'")
        
        x = x1
        y = y1
        for square in rot_face:
            self.canvas.create_rectangle(x, y, x + 33, y + 33, outline = 'black', fill = colors_dict[square])
            x += 33 if x != x1 + 66 else -(x - x1)
            y += 33 if x == x1 else 0
            
    def scramble_cube(self, scramble):
        ''' Read the scramble sequence and pass it into the
            cube's scramble method
            Parameters:
                scramble - sequence of moves (can be a string or a list) '''
        
        scramble_list = None
        
        if type(scramble) is str:
            scramble_list = scramble.split(sep = ' ')
        else:
            scramble_list = scramble
            scramble_canvas = Canvas(self.root, width = 450, height = 50)
            scramble_canvas.place(x = 100, y = 0, anchor = NW)
            scramble_canvas.create_text(5, 10, text = self.scramble_to_str(scramble), anchor = NW, font = ('Times', 20), justify = CENTER)
            
            
        self.cube.scramble(scramble_list)
        
        self.canvas.delete('all')
        self.display_cube()
        

a_cube = Rubiks_Cube()
#a_cube.scramble(['U', 'R', "D'", 'L2', "D'", 'R2', 'F2', 'D', 'F2', "D'", 'B2', 'R2', "U'", 'L', 'R', 'F', 'D', 'L2', 'R2', "B'"])
#Cross_Solver(a_cube)
inter = Cube_Interface(a_cube)

inter.root.mainloop()
