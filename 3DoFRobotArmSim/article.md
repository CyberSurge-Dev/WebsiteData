Recently, I decided to start learning the basics of linear algebra and Inverse kinematics as a fun pastime during my third-period study hall. What started as something I thought I could learn in less than a week, quickly turned into a 3-week rabbit-hole of backtracking on topics to build up to the final product of a Python simulation of a 3DoF robotic arm. Through this article, I aim to cover my journey of learning this intriguing topic, and show the resources and tools that I used to get a better understanding.

Although I don’t aim for this to be a complete tutorial on inverse kinematics because of my mere surface level understanding of the topic; I hope to cover a few of the misconceptions I made going in, and what to expect if you decide to self-teach yourself as I have.

### What is Inverse Kinematics?
Inverse kinematics is the process of identifying the joint angles/robot configuration that a robot needs to be in for its end-effector or ending position to be in a given desired position in space. To fully understand this, you may find it easier to think of it as the opposite of forward kinematics, the process used to calculate the position of the end-effector in space given the robot configuration. Essentially, if f(x) represents the position of the end-effector, then f-1(x) represents the robot configuration required to reach a desired position in space.

At first glance, these two concepts may sound very similar, which in a way they are as they are both directly related to the other, but the math involved for each one can be dramatically different depending on the type of robot.

### Linear Algebra
Linear algebra is an incredibly powerful mathematical tool across many concepts ranging from robotics, data science, 3D transformations of objects in space, and much more. As used in inverse kinematics, linear algebra is used to represent the robot configuration, and to calculate the forward kinematics equations–used to find the end-effector position given the robots configuration–which are essential in solving for inverse kinematics, which is solving for robot configuration given the end-effector position.

Despite how powerful linear algebra can be in solving linear systems of equations, I initially made the misconception that linear algebra would be the only thing that I needed to solve for inverse kinematics. As it turned out, this could not be further from the truth. Although linear algebra does play a crucial role in fast tracking the forward kinematics needed for IK, primarily with the use of [Denavit–Hartenberg parameters](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters), it still does not remove the complexity of solving for the inverse of the resulting forward kinematics equations.

Although I will not cover linear algebra in this article, I highly recommend watching [3Blue1Brown's series on the essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab), which does an excellent job of not only explaining how to do the math, but also why it works.

### Step 1: Create a kinematic diagram
Before you can do anything, you need to create a diagram of your robot with the joints, axis, and lengths clearly labeled, such as the example below.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfvU__zmo286VCfsiQDnoc6XzRuZ0eGMsi2J1dqwLytiyZX4tgei3xe4PVd2vmwPR_k5r4lxsdcS_-zfXcUs2T9WYKcAJ9L4Z8hD4YCgWJtgOssgYQ2lqW57K8q3LYG0dbhEH6GVQ?key=-MdymOov5STuoP7Hieh9-rs5)

Now that you have your diagram drawn, the next thing you have to do is label it with D-H frames/joint frames. When doing this, there are 4 rules to follow:

1.  The z-axis is the axis of rotation for a revolute joint.
2.  The x-axis must be perpendicular to both the current z-axis and the previous z-axis.
3.  The y-axis is determined from the x-axis and z-axis by using the right-hand coordinate system.
4.  The x-axis must intersect the previous z-axis (rule does not apply to frame 0).

Following these rules, you should end up with a diagram similar to the one below.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcB0hPII7ECG3jpHXzVIoFKMDNxHhVQ_mA88FrJ8fVXwvOWLTKn170FsLk-emnApirHdIkY9gc3tXfM2xJ_uPs_49ZDgB8z9vHvJge0AxRD_0yUWWGqt0l7eOc0lxTuosAwmcwo4g?key=-MdymOov5STuoP7Hieh9-rs5)

This step is essential in properly identifying your DH-Parameters, so if you struggle with this step, I recommend following [this awesome tutorial from Automatic Addison](https://automaticaddison.com/how-to-assign-denavit-hartenberg-frames-to-robotic-arms/) before continuing.

### Step 2: Denavit–Hartenberg parameters
Denavit–Hartenberg parameters, or DH parameters for short are the four parameters associated with the DH convention of using separate reference frames on each joint of a robotic arm. Doing this allows us to solve the forward kinematics of a robot manipulator as a series of linear transformations from each joint/point (or reference frame) to the next. Due to the nature of linear transformations, if you want to create a final forward kinematics equation, you just dot-multiply (essentially multiplication for matrices) the transformations for each joint to get the final transformation matrix for the entire robotic arm.

Now that we have a basic understanding of what DH parameters are, let's take a look at the DH table for the SCARA robotic arm from above and explore the meaning of each of its values.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfQj5_d8hVlYGVFFtqBt-ZUIc-VUesDtIqugxK2XkizWefn8x-jXo0uDx2WW5Ig8cDAAqwOos5ONY6LXjnfb64NRSl8yDduHDv5pLowhEYwxIL9qNv28WbpyK1y8GC9TfKhMguRLw?key=-MdymOov5STuoP7Hieh9-rs5)

(Image sourced from [this article from Automatic Addison on how to find DH parameters]([https://automaticaddison.com/how-to-find-denavit-hartenberg-parameter-tables/](https://automaticaddison.com/how-to-find-denavit-hartenberg-parameter-tables/)))

-   θi or theta_i is the angle from xi-1 to xi around zi
-   αi or alpha_i is the angle from zI-1 to zI around xI
-   rI is the distance from the origin of flame I-1 to frame i along xI
-   dI is the distance from xI-1 to xI along the direction of zI-1
    
This step is just as critical as the first, so if you need additional help in understanding concept, I recommend reading [this article from Automatic Addison] ([https://automaticaddison.com/how-to-find-denavit-hartenberg-parameter-tables/](https://automaticaddison.com/how-to-find-denavit-hartenberg-parameter-tables/)).

### Step 3: Forward Kinematics
Using the table we created in the previous step, we can now create the transformation matrices for each of our joints/reference frames. Luckily this is as simple as entering our values from the the DH table we created into the [homogenous transformation matrix]([https://en.m.wikipedia.org/wiki/Transformation_matrix](https://en.m.wikipedia.org/wiki/Transformation_matrix)) seen below. This represents the transformation between the reference frame of joint i to the reference frame of join i-1.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfqaa3MD1SFavUNjxNGXNZBHGDMef9ReZ8_cSf-sBeeBbRZzZgIXt_db0sfKdA0ubJ0KVO7Z6q-usn0U_pBU7D8AlUZozrOiGVEVwd8mw4IiO4dtXx1WP08ip-G_hpyErn__wWzBg?key=-MdymOov5STuoP7Hieh9-rs5)

r represents the 3x3 rotation transformation matrix, and T (r41, r42, r43) represents the x, y, and z coordinates of the end effector.

The image below shows the transformation matrices for each joint of the SCARA robot from the previous step, as well as the final transformation matrix from the initial frame of reference. This final transformation matrix is achieved by dot multiplying together all of the joint transformation matrices left to right (order does matter).

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfLP-B48u-yYnUyQbryM5Tk5ESQSAI4JGOm6gmYthSTrdGAHYHMBNqX7AG0GMVgqNtulJwSDW6_mtNH1gUCY7YmEb7GyH1Q4zDVpUmkQEdV5RaGdnkmq45IBaEGVO2HqtZzYZNY?key=-MdymOov5STuoP7Hieh9-rs5)

The expressions left in the T (r41, r42, r43) section of our final matrix represent our forward kinematic equations for our robot, being the values x, y, and z for our end effector).

### Step 4: Inverse kinematics
Finally after we have created our kinematic diagram, DH parameters, and transformation matrices can we finally start solving the inverse kinematics.

It was at this point in the process where I decided to explore different forms of robotic manipulators, such as 2 DoF and 3 DoF robotic arms, so for the remainder of this article, we will be exploring the inverse kinematics of these 2 robot styles instead. But don't worry about the switch to a different robot type, as the process above can be applied to just about any revolutable kinematic chain to solve for forward kinematics.

### 2DoF robotic arm in 2D space

To start, let's cover the process of solving for the inverse kinematics given the forward kinematics equations derived from the DH convention process.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf_NmszXM_LArzwG6mgx17XNSosRRcEG5lV4Jz2tzE9VAZUEbs1QhbEN5WQHZch8tfbEvMywg942zCwzKq6fRI9xPNDVwGdA4P9ybgrCwebG52gtPhZ-iYhaVxUQx8EAXbAtpdV8w?key=-MdymOov5STuoP7Hieh9-rs5)

Knowing that
x = a1cos(θ1) + a2cos(θ1 + θ2)
y = a1sin(θ1) + a2sin(θ1 + θ2)

You can solve the inverse kinematics for this simple 2 joint arm by solving the triangle using the law of cosine for phi_2 (ϕ2) and phi_3 (ϕ3) (labeled in the diagram above).

a2 = b2 + c2 - (2bc)cos(A)

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcpH-rvA9P0U92fuL3SoX-soZ4v-NDUhfLdm0y93TSrbUPZ2llBbpbOZ__WJ_48bIhaCxB-fBvpk-rXRldxr6rPZN7hpjqHNaGtTzcq1JEP1_-Glk6l42yxHuf2ItCDMV5f_zTk3Q?key=-MdymOov5STuoP7Hieh9-rs5)

### 3DoF robotic arm in 2D space
Moving from 2Dof to 3Dof presents a new set of challenges for solving the inverse kinematics, simply due to the fact that the joints no longer make a simple triangle for us to solve. To explore this, let's take a look at the forward kinematics equations for the arm below.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeBQTezAj6y51fg2feiVCJubPHybsG10jyy9igXuz_7qGrC1KtnYbAsklO9wy92ii3WYHZoohj559C4t5nO7Kg2eVX7FFHr7vGIdoyrFTqxa2yPKFmyOwPxk2qVIsgGjJaxWM9t?key=-MdymOov5STuoP7Hieh9-rs5)

From following the DH convention process, we know the forward kinematic equations to be:
x = a1cos(θ1) + a2cos(θ1 + θ2) + a3cos(θ1 + θ2 + θ3)
y = a1sin(θ1) + a2sin(θ1 + θ2) + a3sin(θ1 + θ2 + θ3)

Notice anything familiar with these equations? The first part two terms are identical to the forward kinematic equations for the 2DoF arm. So if we can find a way to omit the last term, we can solve the equation for the first two terms identical to the previous example.

In this case, we will use the third joint to determine the approach angle of our end effector, making θ1 + θ2 + θ3 a known value, because adding these angles together will equal the angle of our end effector. So knowing this, we can derive the equations below.

xw = x - a3cos(θ1 + θ2 + θ3)
yw = y - a3sin(θ1 + θ2 + θ3)
θ1 + θ2 + θ3 = End effector angle

Now that we have reduced the math, we can solve the previously hidden triangle.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe8Gn80tx6ABXoYg3nVAUstifP-mi1d4usEhjyac42-zUWey3YFJe7-6UasjS010bAwr07NDOb4w7I14xBvwFh8-ANdQQKSdoN70NP4fheZGWYSq9spub8onn1al3Z7_C1KPNO1fg?key=-MdymOov5STuoP7Hieh9-rs5)
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfACeQ6xu75coMwjFgFx50a9gUOQDc1Lsjk8nMC6CtolnyKu4vmrxbuWdIIuNyhFukIR5UOtHNHpN7P3aeN9S6J7CtlKFfZ0DfwTtYbdgkbVP0ByA_vZxvVUoes5XYkQWXVNT1N?key=-MdymOov5STuoP7Hieh9-rs5)

### Creating a simulation program for 3DoF
After solving the math for the 3DoF arm, I decided to create a simple simulation program to test the math using Python PyGame (see [my previous article](https://cybersurge.dev/Blog/6) for more details).

  

Below is the the code used to calculate the angles transcribed from the on-paper version:  

    x_w = x_f - (a_4 * math.cos(gamma))
    y_w = y_f - (a_4 * math.sin(gamma))

    r = math.sqrt((x_w ** 2) + (y_w ** 2))
    
    phi_2 = math.acos(((r ** 2) + (a_2 ** 2) - (a_3 ** 2)) / (2 * r * a_2))
    phi_1 = math.atan2(y_w, x_w)
    phi_3 = math.acos(((a_2 ** 2) + (a_3 ** 2) - (r ** 2)) / (2 * a_2 * a_3))
    
    # If x_f > 0, switch arm to elbow up position
    if x_f > 0:
	    theta_1 = phi_1 + phi_2 # Change subtraction to addition
	    theta_2 = -(math.pi - phi_3) # Negate θ2 for elbow-up
    else:
	    theta_1 = phi_1 - phi_2 # Default elbow-down
	    theta_2 = math.pi - phi_3 # Default elbow-down
    
    # Compute theta_3 using the desired end-effector orientation
    theta_3 = gamma - (theta_1 + theta_2)


  

And below is the code for the entire program, which is also attached as a .py file to this article.
```
import pygame
import math

# Define the arm segments and angles
segment_lengths = [100, 80, 60]
joint_angles = [45, -30, 20] # Angles in degrees
pixel_scalar = 65
dim = (600, 400)
# Pygame setup
pygame.init()
screen = pygame.display.set_mode(dim)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 24)
base_pos = (dim[0]//2, dim[1]//2)

a_1 = 1 
a_2 = 2  
a_3 = 2
a_4 = 0.5

a_1 *= pixel_scalar
a_2 *= pixel_scalar
a_3 *= pixel_scalar
a_4 *= pixel_scalar

# Function to convert polar to Cartesian coordinates 
    # (adjusted for unit circle direction)
def polar_to_cartesian(length, angle, start_pos):
    x = start_pos[0] + length * math.cos(math.radians(-angle))
    y = start_pos[1] + length * math.sin(math.radians(-angle))
    return int(x), int(y)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    x_f = (mouse_pos[0] - base_pos[0])
    y_f = -(mouse_pos[1] - base_pos[1])
    
    # gamma = math.atan2(y_f, x_f)
    gamma = -math.pi /2
    
    try:
        x_w = x_f - (a_4 * math.cos(gamma))
        y_w = y_f - (a_4 * math.sin(gamma))
        
        r = math.sqrt((x_w ** 2) + (y_w ** 2))

        phi_2 = math.acos(((r ** 2) + (a_2 ** 2) - (a_3 ** 2)) 
            / (2 * r * a_2))
        phi_1 = math.atan2(y_w, x_w)
        phi_3 = math.acos(((a_2 ** 2) + (a_3 ** 2) - (r ** 2)) 
            / (2 * a_2 * a_3))
        
        # If x_f > 0, switch arm to elbow up position
        if x_f > 0:
            theta_1 = phi_1 + phi_2 # Change subtraction to addition
            theta_2 = -(math.pi - phi_3) # Negate θ2 for elbow-up
        else:
            theta_1 = phi_1 - phi_2 # Default elbow-down
            theta_2 = math.pi - phi_3 # Default elbow-down
        # Compute theta_3 using the desired end-effector orientation
        theta_3 = gamma - (theta_1 + theta_2)
        
        # Define the arm segments and angles
        segment_lengths = [a_2, a_3, a_4]
        joint_angles = [math.degrees(theta_1), math.degrees(theta_2),
            math.degrees(theta_3)] 
            # Angles in degrees
    
    except Exception:
        theta_1 = 120
        theta_2 = -100
        theta_3 = -45
        
        segment_lengths = [a_2, a_3, a_4] 
        joint_angles = [theta_1, theta_2, theta_3]
    
    screen.fill(WHITE)
    
    # Draw the robotic arm
    current_pos = base_pos
    total_angle = 0
    
    for i in range(len(segment_lengths)):
        total_angle += joint_angles[i]
        next_pos = polar_to_cartesian(segment_lengths[i], 
            total_angle, current_pos)
        pygame.draw.line(screen, BLUE, current_pos, next_pos, 5)
        pygame.draw.circle(screen, RED, next_pos, 8)
    
        current_pos = next_pos
    
    # Draw base
    pygame.draw.circle(screen, RED, base_pos, 10)
    
    # Display end effector and target position
    end_effector_pos = current_pos
    
    # theta_add_text = font.render(f"theta add: 
        {math.degrees(theta_1+theta_2+theta_3):.6}", True, BLACK)
    gamma_text = font.render(f"gamma: {math.degrees(math.atan2(y_f, x_f)):.6}",
        True, BLACK)
    end_effector_text = font.render(f"End Effector: {end_effector_pos}", 
        True, BLACK)
    target_text = font.render(f"Target: {mouse_pos}", True, BLACK)
    
    theta_text = font.render(f"Theta 1: {round(joint_angles[0], 2)}°, 
        Theta 2: {round(joint_angles[1], 2)}°, 
        Theta 3: {round(joint_angles[2], 2)}°", True, BLACK)
    
    # screen.blit(theta_add_text, (10, dim[1]-110)) 
    screen.blit(gamma_text, (10, dim[1] - 90))
    screen.blit(end_effector_text, (10, dim[1] - 70))
    screen.blit(target_text, (10, dim[1] - 50))
    screen.blit(theta_text, (10, dim[1] - 30))
    

    pygame.display.flip()
    
    clock.tick(60)
pygame.quit()
```

### Conclusion

What started as a quick study hall project spiraled into an in-depth dive into linear algebra, kinematics, and robotics. Along the way, I discovered that inverse kinematics isn't just about crunching equations — it's about understanding how robots "think" and move, from creating kinematic diagrams to deriving transformation matrices and solving complex systems of equations. Each step built upon the last, deepening my understanding and making me appreciate the elegance behind robotic motion.

Although I only scratched the surface, this journey taught me that even the most complex topics can be broken down into manageable steps — and that mistakes and misconceptions are part of the learning process. If you're thinking of tackling inverse kinematics yourself, I encourage you to dive in, embrace the challenges, and enjoy the problem-solving journey.

Please take the time to look through the resources attached, as each one has greatly aided me in my process of understanding this subject.


