import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random

class Turtle3D:
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.hx, self.hy, self.hz = 0, 0, 1 
        self.lx, self.ly, self.lz = 1, 0, 0 
        self.ux, self.uy, self.uz = 0, 1, 0 
        self.stack = []
        self.lines = []
    
    def forward(self, length):
        new_x = self.x + self.hx * length
        new_y = self.y + self.hy * length
        new_z = self.z + self.hz * length
        
        self.lines.append(((self.x, self.y, self.z), (new_x, new_y, new_z)))
        self.x, self.y, self.z = new_x, new_y, new_z
    
    def rotate_yaw(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        new_hx = self.hx * cos_a + self.lx * sin_a
        new_hy = self.hy * cos_a + self.ly * sin_a
        new_hz = self.hz * cos_a + self.lz * sin_a
        
        new_lx = -self.hx * sin_a + self.lx * cos_a
        new_ly = -self.hy * sin_a + self.ly * cos_a
        new_lz = -self.hz * sin_a + self.lz * cos_a
        
        self.hx, self.hy, self.hz = new_hx, new_hy, new_hz
        self.lx, self.ly, self.lz = new_lx, new_ly, new_lz
    
    def rotate_pitch(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        new_hx = self.hx * cos_a + self.ux * sin_a
        new_hy = self.hy * cos_a + self.uy * sin_a
        new_hz = self.hz * cos_a + self.uz * sin_a
        
        new_ux = -self.hx * sin_a + self.ux * cos_a
        new_uy = -self.hy * sin_a + self.uy * cos_a
        new_uz = -self.hz * sin_a + self.uz * cos_a
        
        self.hx, self.hy, self.hz = new_hx, new_hy, new_hz
        self.ux, self.uy, self.uz = new_ux, new_uy, new_uz
    
    def rotate_roll(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        new_ux = self.ux * cos_a + self.lx * sin_a
        new_uy = self.uy * cos_a + self.ly * sin_a
        new_uz = self.uz * cos_a + self.lz * sin_a
        
        new_lx = -self.ux * sin_a + self.lx * cos_a
        new_ly = -self.uy * sin_a + self.ly * cos_a
        new_lz = -self.uz * sin_a + self.lz * cos_a
        
        self.ux, self.uy, self.uz = new_ux, new_uy, new_uz
        self.lx, self.ly, self.lz = new_lx, new_ly, new_lz
    
    def push(self):
        self.stack.append((self.x, self.y, self.z, 
                          self.hx, self.hy, self.hz,
                          self.lx, self.ly, self.lz,
                          self.ux, self.uy, self.uz))
    
    def pop(self):
        (self.x, self.y, self.z, 
         self.hx, self.hy, self.hz,
         self.lx, self.ly, self.lz,
         self.ux, self.uy, self.uz) = self.stack.pop()

def generate_commands():
    axiom = "X"
    
    rules = {
        "X": "F[+X][-X][&X][^X][/X][\\X]",
        "F": "FF"
    }
    
    current = axiom
    for i in range(6):
        next_str = ""
        for char in current:
            if char in rules:
                next_str += rules[char]
            else:
                next_str += char
        current = next_str
    return current

def draw_tree():
    step = 0.35         
    angle = 35
    
    commands = generate_commands()
    turtle = Turtle3D()
    angle_rad = angle * math.pi / 180
    
    count = 0
    for cmd in commands:
        if cmd == 'F':
            turtle.forward(step)
            count += 1
            if count % 1000 == 0:
                pass
        elif cmd == '+':
            turtle.rotate_yaw(angle_rad)
        elif cmd == '-':
            turtle.rotate_yaw(-angle_rad)
        elif cmd == '&':
            turtle.rotate_pitch(angle_rad)
        elif cmd == '^':
            turtle.rotate_pitch(-angle_rad)
        elif cmd == '/':
            turtle.rotate_roll(angle_rad)
        elif cmd == '\\':
            turtle.rotate_roll(-angle_rad)
        elif cmd == '[':
            turtle.push()
        elif cmd == ']':
            turtle.pop()
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for start, end in turtle.lines:
        ax.plot([start[0], end[0]], 
                [start[1], end[1]], 
                [start[2], end[2]], 
                color='#5D3A1A', linewidth=2, alpha=0.9)
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('3D Дерево', fontsize=14)
    
    all_points = []
    for start, end in turtle.lines:
        all_points.append(start)
        all_points.append(end)
    
    if all_points:
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        zs = [p[2] for p in all_points]
        
        margin = 2
        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - 0.5, max(ys) + margin)
        ax.set_zlim(min(zs) - margin, max(zs) + margin)
    
    ax.view_init(elev=20, azim=-55)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    draw_tree()
