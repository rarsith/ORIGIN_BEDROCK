"""
Convert Between VtArray and Numpy Array
Some Attributes store array type data which are accessed using the VtArray classes. You can find a list of the VtArray classes in our USD Data Types documentation

If you need to manipulate the arrays using Python, it is advantageous to use Numpy to benefit from it’s speed and efficiency. These code samples show how you can convert between the VtArray objects and Numpy Array objects.

Note

These examples show how to convert using only the Vt.Vec3fArray class, but the same can be applied to any VtArray class. See what other VtArray classes exist in the USD Data Types documentation.


USD Python
Convert to Numpy Array

To convert a VtArray to a Numpy Array, simply pass the VtArray object to numpy.array constructor.
"""

import numpy
from pxr import Vt


def convert_vt_to_np(my_array: Vt.Vec3fArray) -> numpy.ndarray:
    return numpy.array(my_vec3_array)


#############
# Full Usage
#############

# Create a Vt.Vec3fArray and convert it to a numpy array
my_vec3_array = Vt.Vec3fArray([(1,2,3),(4,5,6),(7,8,9)])
np_array: numpy.ndarray = convert_vt_to_np(my_vec3_array)

# print the numpy array to check the values
print(np_array)

# check the size and length of the numpy array
assert np_array.size == 9
assert len(np_array) == 3

"""
Convert from Numpy Array

To convert a Numpy Array to a VtArray, you can use FromNumpy() from the VtArray class you want to convert to.

"""

import numpy
from pxr import Vt


def convert_np_to_vt(my_array: numpy.ndarray) -> Vt.Vec3fArray:
    return Vt.Vec3fArray.FromNumpy(my_array)


#############
# Full Usage
#############

# Create a numpy array and convert it into a Vt.Vec3fArray
np_array = numpy.array([(1,2,3),(4,5,6),(7,8,9)])
from_numpy: Vt.Vec3fArray = convert_np_to_vt(np_array)

# Print the Vt.Vec3fArray to check the values
print(from_numpy)

# Check the length of the numpy array
assert len(np_array) == 3