# Parser for a simple language to do basic Constructive Solid Geometry
 - Enables generation of images by combining simple shapes using operations like union, intersection, subtraction.
 - Visualize the generation process as a tree.

## Implementation
Implemented in python 3.6 using PLY, pydot and other standard python libraries.

## Grammar
 - Write simple postfix notation
 - Operations may be one of the following --> Union: ```+```, Intersection: ```*```, Difference: ```-```
 - Operands are of the type '```shape(position_x, position_y, scale)```
 - The supported shapes are --> Circle: ```c```, Triangle: ```t```, Square: ```s```
 - position_x, position_y and scale can only be integers
 - Example ```s(32,50,5)t(35,45,7)s(40,10,4)*c(32,54,8)+-```

## Running the Code
 - Write out the required expression in one or more files, say ```filename1.txt```, ```filename2.txt```.
 - Generate the corresponding image by executing ```python main.py filename_1 filename_2```
 - For generating random expressions and their corresponding visualisation, run ```python main.py``` without a filename following it.
 
## Managing Parameters 
 - Control the number of random samples by changing the ```numexs``` variable and the number of operands in the random expressions by changing the ```numops``` variable in main.py.
 - Canvas size can be controlled through the ```canvas_shape``` variable in canvasops.py
 - The path variable determines where the generated files are stored for random expressions. If the expressions are provided in a file then the visualisations are generated in the folder containing the expressions file, irrespective of the value of path.
 - The restrictions on the random expressions can be found and changed in canvasops.py
 - If the tree visualisations are not required, set ```visualize``` in grammar.py to False.
 
### Note:
The visualisation process creates temporary files of the form ```tempNUM.png``` (where NUM can be any number) and then deletes them. If any file of that form exists in the concerned folder, it will be deleted.
