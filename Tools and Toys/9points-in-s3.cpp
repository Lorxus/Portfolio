// Given a number n, and a number of trials t, this program looks for the set of n points on the 3-sphere (glome) whose maximum cosine similarity is minimized among all t of the trials, that is, the set of such points which is as pairwise distant as possible, or equivalently, the set of n vectors whose minimum angle separation is still as close as possible to 90* (for n >= 2*dimension).
// https://mathoverflow.net/questions/24864/almost-orthogonal-vectors
// It does this by:
// 1. Naively randomly (distribution = N(0,1)) generating a 4-tuple of coordinates and then normalizing the result. This gives us a single uniformly random point from the glome.
// 2. Doing step 1 another n-1 times. This gives us a set of n points scattered over the glome.
// 3. Pairwise checking the cosine similarity of points from the set of n points, checking whether this is a new best, and storing it if so. At the end of the t trial runs, this gives us a number - the maximum pairwise dot-product of any two of the vectors/points we generated - and the set of coordinates of the points.

#include <array>
#include <cmath>
#include <Eigen/Dense>
#include <iostream>
#include <numeric>
#include <random>

// declare a normal-distribution random generator
std::random_device rd;
std::mt19937 generator(rd());
std::normal_distribution<float> distribution(0.0f, 1.0f);

// print off the coordinates of a given point
void print_point(const std::array<float, 4>& pt) {
    std::cout << "(" << pt[0] << ", " << pt[1] << ", " << pt[2] << ", " << pt[3] << ")" << std::endl;
}

// normalize a given vector
std::array<float, 4> normalize(std::array<float, 4> point) {
    float length = 0.0f;
    for (int i = 0; i < 4; i++) {
        length += pow(point[i], 2);
    }
    length = sqrt(length);
    
    for (int i = 0; i < 4; i++) {
        point[i] = point[i]/length;
    }
    return point;
}

// generate a point on S^3
std::array<float, 4> samplepoint() {
    std::array<float, 4> mypoint;

    for (int i = 0; i < 4; i++) {
        mypoint[i] = distribution(generator);
    }

    return normalize(mypoint);
}

void run_glome_search() {    
    // accept input - number of points, number of runs, bounds for rejection
    std::cout << "How many unit vectors do we want to fit on this glome? (Try 9!)" << std::endl;
    int numpoints;
    std::cin >> numpoints;

    std::cout << "How many times shall we go looking?" << std::endl;
    int numruns;
    std::cin >> numruns;

    std::cout << "What should our bounds of immediate rejection and retry be, in terms of cosine similarity? (0.162 is the theoretical min for 9 points; realistically try 0.7 or so or this will take a long time..." << std::endl;
    float min_bad_cossim;
    std::cin >> min_bad_cossim;
    min_bad_cossim = std::min(min_bad_cossim, 1.0f);

    std::cout << "\n\n";

    // initialize array of best points, best min cosine similarity, and run count
    float bestglomepoints[numpoints][4];
    float mostorthogdp = 1;
    int runcount = 0;
    
    for (int i = 0; i < numruns; i++) {
        float glomepoints[numpoints][4];
        runcount++;
        
        for (int j = 0; j < numpoints; j++) {
            auto temp_pt = samplepoint();
            // print_point(temp_pt);
            for (int k = 0; k < 4; k++) {
                glomepoints[j][k] = temp_pt[k];
            }
            // I could, if I wanted to, fix one of the points to be (say) the north pole (0, 0, 0, 1) WLOG...
        }

        float maxdotprodthisrun = -1.0f;
        
        for (int idx1 = 0; idx1 < numpoints - 1; idx1++) {
            float vecA[4];
            for (int tempA = 0; tempA < 4; tempA++) {
                vecA[tempA] = glomepoints[idx1][tempA];
            }

            for (int idx2 = idx1 + 1; idx2 < numpoints; idx2++) {
                float vecB[4];
                for (int tempB = 0; tempB < 4; tempB++) {
                    vecB[tempB] = glomepoints[idx2][tempB];
                }
                
                // float dotprod = std::inner_product(vecA.begin(), vecA.end(), vecB.begin(), 0);
                // Above doesn't work, so calculate the dot product manually

                float dotprod = 0.0f;
                for (int dpidx = 0; dpidx < 4; dpidx++) {
                    dotprod = dotprod + vecA[dpidx] * vecB[dpidx];
                }
                
                if (dotprod > maxdotprodthisrun && dotprod < 0.99) {
                maxdotprodthisrun = dotprod;
                }
            }
        }

        if (maxdotprodthisrun > min_bad_cossim) {
        // if maxdotprodthisrun > 0.8:
        // theoretical min for 9 points is ~0.162 at degree separation of ~80.68*, but a random-esque search like this one rarely finds anything 
            i--;
            // std::cout << i << runcount << maxdotprodthisrun << std::endl;
            continue;
        }
        if (maxdotprodthisrun < mostorthogdp) { // report a new best and update bestglomepoints
            std::cout << "Better repulsive-covering of the glome found for " << numpoints << " points on run " << runcount << " (run index " << i << "); max dotproduct is now: " << maxdotprodthisrun << "." << std::endl;
            mostorthogdp = maxdotprodthisrun;

            for (int j = 0; j < numpoints; j++) {
                for (int k = 0; k < 4; k++) {
                    bestglomepoints[j][k] = glomepoints[j][k];
                }
            }
        }
    }

    // Finish up - report true run count, best set of points, worst/largest dot product for that set
    std::cout << "Ending true run count: " << runcount << "." << std::endl;

    float angle_degrees = std::acos(mostorthogdp) * 180.0f / M_PI;
    std::cout << "\nThe best set of " << numpoints << " points found after " << numruns 
          << " runs had maximum mutual dotproduct of " << mostorthogdp 
          << " (angle: " << angle_degrees << " degrees)!\n" << std::endl;

    // Report the coordinates
    std::cout << "Listing off the coordinates:\n";
    for (int idx = 0; idx < numpoints; idx ++) {
        for (int coord = 0; coord < 4; coord ++) {
        std::cout << bestglomepoints[idx][coord] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    std::cout << "=====A TINDALOSIAN FOX NEEDS GEOMETRY TREATS FOR A SHINY COAT=====" << std::endl;
    run_glome_search();
    std::cout << "=====THANK YOU FOR EXPLORING HIGHER-DIMENSIONAL GEOMETRY WITH ME! ^w^=====" << std::endl;
    return 0;
}