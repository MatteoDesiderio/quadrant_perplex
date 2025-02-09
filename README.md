Works with any Perple_X version, if build, vertex, werami, perplex_option and database/solution model files are supplied

# Description

 A few simple python modules and shell scripts to

* Define a number of quadrants in the PT space
* Run BUILD for each of these quadrants, automating the input
* Run VERTEX in each of these automating the input and possibly parallelizing
* Run WERAMI, automating the input
* Stitch the tab files thus created into one neat tab file


# Usage

Make sure a directory with the name of the Perple_X version you want to use exists. 
Contents of the folder:

	- build, vertex, werami executables 
	- perplex_option file 
	- database/solution model
of the relevant version.

Create txt file with components, mass amounts, solution models 
(check template for how it's done):
```
vim template.txt
```

Then:
```
python split.py template.txt n_sub
```
Where n_sub is the number of quadrants along each axis. (i.e., the number of times that build, vertex and werami will be performed is n = n_sub^2) 

Then:
```
./parallelize build template n_proc
./parallelize vertex template n_proc
./parallelize werami template n_proc
```
Note: need to wait for vertex to finish before you can do werami, 
same thing for vertex and build but the latter is almost instantaneous.

You may take a gander at the progress with 
```
tail -f template/quadrant*/OUTPUT_*txt
```

Finally:
```
python unsplit.py template
```
This will put everything together. You can check out the result with pywerami.
