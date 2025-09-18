# Some satellite operators of knots
> Warning: I believe it currently does not work for links with more than one components.

This repository provides the following satellite operators of knots, to be used with [SnapPy](https://snappy.computop.org)
    
- ```whitehead_double(snappy_knot, framing = 0, do_simplify = False)``` 
    - which returns the Whitehead double of a given knot (as an instance of ```snappy.Link```).
- ```parallel(m, n, snappy_knot, framing = 0, do_simplify = False)``` 
    - which returns the $(m,n)$-parallel (also called $(m,n)$-cable) of a give knot.

The variable ```framing``` controls the frame on the input knot diagram, 
in the way that it adds Reidemester I moves such that the writhe of the diagram is equal to the value of framing. 

As an example, the following is the $(8,3)$-parallel of the $0$-framed trefoil drawn with
````
parallel(8, 3, snappy.Link('3_1')).view()
````

![Failed to display image; see parallel(8,3, 3_1).pdf under the repository instead](./parallel(8,3,%203_1).png "The (8,3)-parallel of 0-framed trefoil")