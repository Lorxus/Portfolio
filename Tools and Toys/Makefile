TARGET = 9points-in-s3
CXX = g++
# Add the -I flag with the path to the directory containing the 'Eigen' folder
CXXFLAGS = -Wall -g -I C:/Libraries/eigen-5.0.1 

$(TARGET): $(TARGET).cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
