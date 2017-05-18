# Compiler for a simple language to do basic Constructive Solid Geometry
Enable generation of images by combining simple shapes using operations like union, intersection, subtraction.


## Implementation
Implemented in python using PLY and other standard libraries.

## Grammar
 - Write simple postfix notation
 - Operations may be one of the following --> Union: ```+```, Intersection: ```*```, Difference: ```-```
 - Operands are of the type '```shape(position_x, position_y, scale)```
 - The supported shapes are --> Circle: ```c```, Triangle: ```t```, Square: ```s```
 - position_x, position_y and scale can only be integers
 - Example ```s(32,50,5)t(35,45,7)s(40,10,4)*c(32,54,8)+-```

## Running the Code
 - Write out the required expression in a file, say ```filename1.txt```
 - Generate the corresponding image by executing ```./main.py filename_1```
