# Given a number n, and a number of trials t, this program looks for the set of n points on the 3-sphere (glome) whose maximum cosine similarity is minimized among all t of the trials, that is, the set of such points which is as pairwise distant as possible, or equivalently, the set of n vectors whose minimum angle separation is still as close as possible to 90* (for n >= 2*dimension).
# https://mathoverflow.net/questions/24864/almost-orthogonal-vectors
# It does this by:
# 1. Naively randomly (distribution = N(0,1)) generating a 4-tuple of coordinates and then normalizing the result. This gives us a single uniformly random point from the glome.
# 2. Doing step 1 another n-1 times. This gives us a set of n points scattered over the glome.
# 3. Pairwise checking the cosine similarity of points from the set of n points, checking whether this is a new best, and storing it if so. At the end of the t trial runs, this gives us a number - the maximum pairwise dot-product of any two of the vectors/points we generated - and the set of coordinates of the points.

import numpy as np
import itertools as it

def normalize(L):
    myvector = L[0]
    templen = 0.0
    # print(myvector)
    
    for coord in myvector:
        templen += coord ** 2.0
    
    templen = templen ** 0.5
    # print(templen)
    normalvec = myvector/templen

    return normalvec

def samplepoint(): # generates a random point on S^3
    rand = np.random.default_rng()
    mypoint = rand.normal(0.0, 1.0, size=(1,4))
    mypoint = normalize(mypoint)
    return mypoint

def main():
    print('How many unit vectors do we want to fit on this glome? (Try 9!)')
    numpoints = int(input())
    print('How many times shall we go looking?')
    numruns = int(input())
    print('\n\n')

    bestglomepoints = []
    mostorthogdp = 1
    runcount = 0

    i = 0
    while i < numruns:
        glomepoints = []
        i += 1
        runcount += 1
        
        for j in range(numpoints):
            temp_pt = samplepoint()
            #print(temp_pt)
            glomepoints.append(temp_pt)
            # I could, if I wanted to, fix one of the points to be (say) the north pole (0, 0, 0, 1) WLOG...

        maxdotprodthisrun = -1
        
        for point1, point2 in it.combinations(glomepoints, 2):
            dotprod = np.dot(point1, point2.T)
            if dotprod > maxdotprodthisrun and dotprod != 1:
                maxdotprodthisrun = dotprod
        
        if maxdotprodthisrun > 0.41:
            i = i-1
            print(i, runcount, maxdotprodthisrun)
            continue

        if maxdotprodthisrun < mostorthogdp:
            print('Better repulsive-covering of the glome found for', numpoints, 'points on run', runcount, '; max dotproduct is now:', maxdotprodthisrun)
            mostorthogdp = maxdotprodthisrun
            bestglomepoints = glomepoints
        
    print(runcount)
    print('\nThe best set of', numpoints, 'points found after', numruns, 'runs had maximum mutual dotproduct of', mostorthogdp, '!\n')
    glomecoords = []
    for i in bestglomepoints:
        glomecoords.append(i)
    print('Listing off the coordinates:\n')
    for i in glomecoords:
        print(i)

if __name__ == "__main__":
    print('=====A TINDALOSIAN FOX NEEDS GEOMETRY TREATS FOR A SHINY COAT=====')
    main()
    print('=====THANK YOU FOR EXPLORING HIGHER-DIMENSIONAL GEOMETRY WITH ME! ^w^=====')
