'''
This file contains the Rubiks_Cube class which represents a functioning 3x3 Rubik's Cube puzzle

Acronyms:
OLL - Orientation of the Last Layer
PLL - Permutation of the Last Layer
F2L - First 2 Layers
AUF - Alignment of the U-Face

Author: Henry Ham

Version: 2022.04.25
'''

str_dict = {0:'U: ', 1:'F: ', 2:'R: ', 3:'B: ', 4:'L: ', 5:'D: '}
''' maps values of i variable in __str__ to a string to avoid hassle of conditionals '''

class Rubiks_Cube:
    ''' This class represents a model of a Rubik's Cube puzzle
        that can be turned and scrambled '''
    
    def __init__(self):
        ''' Initializes the cube into a solved state
            
            Each face of the cube is represented by a list of numbers
            which represent certain colors as follows:
            
            0 = white
            1 = green
            2 = red
            3 = blue
            4 = orange
            5 = yellow '''
        
        self.U = [0] * 9
        self.F = [1] * 9
        self.R = [2] * 9
        self.B = [3] * 9
        self.L = [4] * 9
        self.D = [5] * 9
        
        self.cube = [self.U, self.F, self.R, self.B, self.L, self.D]
        
    def __str__(self):
        ''' Returns a printable representation of the cube's
            current state '''
        result = ''
        
        for i in range(6):
            face = str_dict[i]
            count = 1
            for square in self.cube[i]:
                face += '[' + str(square) + ']'
                if count % 3 == 0:
                    face += '\n   '
                count += 1
            result += face[:-3] + '\n'
        
        return result
    
    def clone(self):
        ''' Returns a separate cube object that is a clone
            of this one
            Returns: clone of this cube '''
        
        clone = Rubiks_Cube()
        
        for i in range(6):
            for j in range(9):
                clone.cube[i][j] = self.cube[i][j]
        
        return clone
    
    def get_hint(self):
        ''' Read the current state of the cube and return
            the correct hint
            Returns: hint about the next step to
                solving the cube '''
        
        if not self.check_F2L():
            return 'F2L not ready for hints yet!'
        elif self.check_top_layer() == 'OLL1':
            return self.get_OLL_first_look()
        elif self.check_top_layer() == 'OLL2':
            return self.get_OLL_second_look()
        else:
            return 'PLL not ready for hints yet!'
    
    def get_OLL_first_look(self):
        ''' Get the first part of the 2-look OLL algorithm
            for the current state of the cube
            Returns: algorithm as a string '''
        
        # check for dot-case
        top_edges = [self.U[1], self.U[3], self.U[5], self.U[7]]
        if self.U[4] not in top_edges:
            return "F (R U R' U') S (R U R' U') f'"
        
        count = 0
        for i in range(4):
            AUF_str = "(U) " if count == 1 else "(U2) " if count == 2 else "(U') " if count == 3 else ""
            # check for v-case
            if self.U[5] == self.U[4] == self.U[7]:
                self.undo_AUF(count) 
                return AUF_str + "f (R U R' U') f'"
            if self.U[3] == self.U[4] == self.U[5]:
                self.undo_AUF(count)
                return AUF_str + "F (R U R' U') F'"
            self.move("U")
            count += 1
            
    def get_OLL_second_look(self):
        ''' Get the second part of the 2-look OLL algorithm
            for the current state of the cube
            Returns: algorithm as a string '''
        
        oriented_corners = 0
        top_corners = [self.U[0], self.U[2], self.U[6], self.U[8]]
        for corner in top_corners:
            if corner == self.U[4]:
                oriented_corners += 1
        
        count = 0
        for i in range(4):
            AUF_str = "(U) " if count == 1 else "(U2) " if count == 2 else "(U') " if count == 3 else ""
            if oriented_corners == 0:
                # check for case 1
                if self.F[0] == self.F[2] == self.U[4] == self.B[0] == self.B[2]:
                    self.undo_AUF(count)
                    return AUF_str + "R U2 R' U' R U R' U' R U' R'"
                # check for case 2
                elif self.L[0] == self.L[2] == self.U[4] == self.F[2] == self.B[0]:
                    self.undo_AUF(count)
                    return AUF_str + "R U2 R2 U' R2 U' R2 U2 R"
            elif oriented_corners == 1:
                # check for case 1
                if self.U[2] == self.U[4] == self.L[0] == self.F[0] == self.R[0]:
                    self.undo_AUF(count)
                    return AUF_str + "R U2 R' U' R U' R'"
                # check for case 2
                elif self.U[6] == self.U[4] == self.F[2] == self.R[2] == self.B[2]:
                    self.undo_AUF(count)
                    return AUF_str + "R U R' U R U2 R'"
            elif oriented_corners == 2:
                # check for case 1
                if self.U[0] == self.U[2] == self.U[4] == self.F[0] == self.F[2]:
                    self.undo_AUF(count)
                    return AUF_str + "R2 D R' U2 R D' R' U2 R'"
                # check for case 2
                elif self.U[2] == self.U[8] == self.U[4] == self.B[2] == self.F[0]:
                    self.undo_AUF(count)
                    return AUF_str + "r U R' U' r' F R F'"
                # check for case 3
                elif self.U[2] == self.U[6] == self.U[4] == self.L[0] == self.F[2]:
                    self.undo_AUF(count)
                    return AUF_str + "F' r U R' U' r' F R"
            self.move("U")
            count += 1
            
            
    def check_F2L(self):
        ''' Check if the first 2 layers have been solved
            Returns: True if F2L is complete '''
        
        return self.F[3] == self.F[4] == self.F[5] == self.F[6] == self.F[7] == self.F[8] \
            and self.R[3] == self.R[4] == self.R[5] == self.R[6] == self.R[7] == self.R[8] \
            and self.B[3] == self.B[4] == self.B[5] == self.B[6] == self.B[7] == self.B[8] \
            and self.L[3] == self.L[4] == self.L[5] == self.L[6] == self.L[7] == self.L[8] \
            
    def check_top_layer(self):
        ''' Check if all top-layer edges are oriented
            Returns: 'OLL1' if top cross not solved, OLL2 if
                top cross is solved, or 'PLL' if top face is complete '''
        
        solved_top = [self.U[4]] * 9
        if self.U == solved_top:
            return 'PLL'
        elif self.U[1] == self.U[3] == self.U[4] == self.U[5] == self.U[7]:
            return 'OLL2'
        else:
            return 'OLL1'
            
    def undo_AUF(self, count):
        ''' undo all top-layer turns done to find an OLL or PLL case
            Parameters:
                count: number of U turns to undo '''
        
        for i in range(count):
            self.move("U'")
        
    
    def reset(self):
        ''' Reset the cube to a solved state '''
        
        self.U = [0] * 9
        self.F = [1] * 9
        self.R = [2] * 9
        self.B = [3] * 9
        self.L = [4] * 9
        self.D = [5] * 9
    
    def copy_face(self, face):
        ''' Copy the passed face into a separate list and
            return it
            Parameters:
                face - face to copy
            Returns: copy of face '''
        
        return list(face)
    
    def get_face(self, face):
        ''' Get the passed face name as a string
            Parameters:
                face - face to get the name of
            Returns: face name '''
        
        if face == self.U:
            return 'U'
        elif face == self.F:
            return 'F'
        elif face == self.R:
            return 'R'
        elif face == self.B:
            return 'B'
        elif face == self.L:
            return 'L'
        else:
            return 'D'
    
    def scramble(self, scramble):
        ''' Takes a list of move strings and executes them
            all in order
            Parameters:
                scramble - list of move strings '''
        
        for move in scramble:
            self.move(move)
    
    def move(self, move):
        ''' Move the cube based on the move input
            Parameters:
                move - Specified move as a string in cube notation '''
        
        # maps cube notation inpute to the method corresponding to that move
        moves_dict = {"R":self.move_R, "L":self.move_L, "F":self.move_F, "B":self.move_B, "U":self.move_U, "D":self.move_D, \
                      "M":self.move_M, "S":self.move_S, "E":self.move_E, 'x':self.move_x, 'y':self.move_y, 'z':self.move_z, \
                      "r":self.move_r, "l":self.move_l, "f":self.move_f, "b":self.move_b, "u":self.move_u, "d":self.move_d}
        
        if len(move) == 2:
            if move[1] == "2":
                for i in range(2):
                    moves_dict[move[0]]()
            elif move[1] == "'":
                for i in range(3):
                    moves_dict[move[0]]()
        else:
            moves_dict[move]()
            
    def move_z(self):
        ''' Rotate the entire cube 90° clockwise along the F face '''
        
        self.move("F")
        self.move("S")
        self.move("B'")
            
    def move_x(self):
        ''' Rotate the entire cube 90° clockwise along the R face '''
        
        self.move("R")
        self.move("M'")
        self.move("L'")
        
    def move_y(self):
        ''' Rotate the entire cube 90° along the U face '''
        
        self.move("U")
        self.move("E'")
        self.move("D'")
        
    def move_r(self):
        ''' Makes a wide R move '''
        
        self.move("R")
        self.move("M'")
            
    def move_l(self):
        ''' Makes a wide L move '''
        
        self.move("L")
        self.move("M")
        
    def move_f(self):
        ''' Makes a wide F move '''
        
        self.move("F")
        self.move("S")
        
    def move_b(self):
        ''' Makes a wide B move '''
        
        self.move("B")
        self.move("S'")
        
    def move_u(self):
        ''' Makes a wide U move '''
        
        self.move("U")
        self.move("E'")
        
    def move_d(self):
        ''' Makes a wide D move '''
        
        self.move("D")
        self.move("E")
    
    def move_M(self):
        ''' Moves the middle slice of the cube 90° clockwise '''
        
        self.U[1], self.U[4], self.U[7], self.F[1], self.F[4], self.F[7], \
                   self.D[1], self.D[4], self.D[7], self.B[7], self.B[4], self.B[1] = \
                   self.B[7], self.B[4], self.B[1], self.U[1], self.U[4], self.U[7], \
                   self.F[1], self.F[4], self.F[7], self.D[1], self.D[4], self.D[7]
        
    def move_S(self):
        ''' Moves the standing slice of the cube 90° clockwise '''
        
        self.U[3], self.U[4], self.U[5], self.R[1], self.R[4], self.R[7], \
                   self.D[5], self.D[4], self.D[3], self.L[7], self.L[4], self.L[1] = \
                   self.L[7], self.L[4], self.L[1], self.U[3], self.U[4], self.U[5], \
                   self.R[1], self.R[4], self.R[7], self.D[5], self.D[4], self.D[3]
        
    def move_E(self):
        ''' Moves the equatorial slice of the cube 90° clockwise '''
        
        self.F[3], self.F[4], self.F[5], self.R[3], self.R[4], self.R[5], \
                   self.B[3], self.B[4], self.B[5], self.L[3], self.L[4], self.L[5] = \
                   self.L[3], self.L[4], self.L[5], self.F[3], self.F[4], self.F[5], \
                   self.R[3], self.R[4], self.R[5], self.B[3], self.B[4], self.B[5]
    
    def move_R(self):
        ''' Moves the right face of the cube 90° clockwise '''
        
        self.F[2], self.F[5], self.F[8], self.U[2], self.U[5], self.U[8], \
                   self.B[0], self.B[3], self.B[6], self.D[2], self.D[5], self.D[8] = \
                   self.D[2], self.D[5], self.D[8], self.F[2], self.F[5], self.F[8], \
                   self.U[8], self.U[5], self.U[2], self.B[6], self.B[3], self.B[0]
        
        self.R[0], self.R[1], self.R[2], self.R[3], self.R[4], self.R[5], self.R[6], self.R[7], self.R[8] = \
                   self.R[6], self.R[3], self.R[0], self.R[7], self.R[4], self.R[1], self.R[8], self.R[5], self.R[2]
    
    def move_L(self):
        ''' Moves the left face of the cube 90° clockwise '''
        
        self.F[0], self.F[3], self.F[6], self.D[0], self.D[3], self.D[6], \
                   self.B[8], self.B[5], self.B[2], self.U[0], self.U[3], self.U[6] = \
                   self.U[0], self.U[3], self.U[6], self.F[0], self.F[3], self.F[6], \
                   self.D[0], self.D[3], self.D[6], self.B[8], self.B[5], self.B[2]
        
        self.L[0], self.L[1], self.L[2], self.L[3], self.L[4], self.L[5], self.L[6], self.L[7], self.L[8] = \
                   self.L[6], self.L[3], self.L[0], self.L[7], self.L[4], self.L[1], self.L[8], self.L[5], self.L[2]
        
    def move_F(self):
        ''' Moves the front face of the cube 90° clockwise '''
        
        self.U[6], self.U[7], self.U[8], self.R[0], self.R[3], self.R[6], \
                   self.D[2], self.D[1], self.D[0], self.L[8], self.L[5], self.L[2] = \
                   self.L[8], self.L[5], self.L[2], self.U[6], self.U[7], self.U[8], \
                   self.R[0], self.R[3], self.R[6], self.D[2], self.D[1], self.D[0]
        
        self.F[0], self.F[1], self.F[2], self.F[3], self.F[4], self.F[5], self.F[6], self.F[7], self.F[8] = \
                   self.F[6], self.F[3], self.F[0], self.F[7], self.F[4], self.F[1], self.F[8], self.F[5], self.F[2]
        
    def move_B(self):
        ''' Moves the back face of the cube 90° clockwise '''
        
        self.U[2], self.U[1], self.U[0], self.L[0], self.L[3], self.L[6], \
                   self.D[6], self.D[7], self.D[8], self.R[8], self.R[5], self.R[2] = \
                   self.R[8], self.R[5], self.R[2], self.U[2], self.U[1], self.U[0], \
                   self.L[0], self.L[3], self.L[6], self.D[6], self.D[7], self.D[8]
        
        self.B[0], self.B[1], self.B[2], self.B[3], self.B[4], self.B[5], self.B[6], self.B[7], self.B[8] = \
                   self.B[6], self.B[3], self.B[0], self.B[7], self.B[4], self.B[1], self.B[8], self.B[5], self.B[2]
        
    def move_U(self):
        ''' Moves the top face of the cube 90° clockwise '''

        self.F[2], self.F[1], self.F[0], self.L[2], self.L[1], self.L[0], \
                   self.B[2], self.B[1], self.B[0], self.R[2], self.R[1], self.R[0] = \
                   self.R[2], self.R[1], self.R[0], self.F[2], self.F[1], self.F[0], \
                   self.L[2], self.L[1], self.L[0], self.B[2], self.B[1], self.B[0]
        
        self.U[0], self.U[1], self.U[2], self.U[3], self.U[4], self.U[5], self.U[6], self.U[7], self.U[8] = \
                   self.U[6], self.U[3], self.U[0], self.U[7], self.U[4], self.U[1], self.U[8], self.U[5], self.U[2]
        
    def move_D(self):
        ''' Moves the bottom face of the cube 90° clockwise '''

        self.F[6], self.F[7], self.F[8], self.R[6], self.R[7], self.R[8], \
                   self.B[6], self.B[7], self.B[8], self.L[6], self.L[7], self.L[8] = \
                   self.L[6], self.L[7], self.L[8], self.F[6], self.F[7], self.F[8], \
                   self.R[6], self.R[7], self.R[8], self.B[6], self.B[7], self.B[8]
        
        self.D[0], self.D[1], self.D[2], self.D[3], self.D[4], self.D[5], self.D[6], self.D[7], self.D[8] = \
                   self.D[6], self.D[3], self.D[0], self.D[7], self.D[4], self.D[1], self.D[8], self.D[5], self.D[2]
    