# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up
    
def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

    x_axis = len(colors[0])
    y_axis = len(colors)
    q = []
    k = 0
    acc = 0                     #used to accumulating the total probability after sensing 
    
    for move in motions:
        #the robot should move first and sense after
        for j in range(0,y_axis):
            q_temp = []         #temporary list to store our results from moving
            for i in range(0,x_axis):
                s = p_move *p[(j - move[0]) % y_axis][(i - move[1]) % x_axis]
                s = s + (1 - p_move)*p[j][i]
                q_temp.append(s)
                
            q.append(q_temp)
            
        p = list(q)             #first assignment prior to sensing
        q = []                  #reset our q list to be empty as we are going to reuse it
        acc = 0
        #sense after completing its motion
        for j in range(0,y_axis):
            q_temp = []
            for i in range(0,x_axis):
                hit = (measurements[k] == colors[j][i])
                q_temp.append(p[j][i] * (hit * sensor_right + (1 - hit)*(1 - sensor_right)))
                
            acc = acc + sum(q_temp)
            q.append(q_temp)

        #normalize our probability
        for j in range(0,y_axis):
            for i in range(0,x_axis):
                q[j][i] = float(q[j][i]/acc)

        p = list(q)
        q = []
        k = k+1

    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer
