"""
The extraction of the curves from the acv files are from here:
  
  https://github.com/vbalnt/filterizer
"""

import sys
from struct import unpack

import numpy
from PIL import Image
from scipy import interpolate
import cv2


class Filter:

    def __init__(self, acv_file_path, name):
        self.name = name
        with open(acv_file_path, 'rb') as acv_file:
            self.curves = self._read_curves(acv_file)
        self.polynomials = self._find_coefficients()

    def _read_curves(self, acv_file):
        _, nr_curves = unpack('!hh', acv_file.read(4))
        curves = []
        for i in range(0, nr_curves):
            curve = []
            num_curve_points, = unpack('!h', acv_file.read(2))
            for j in range(0, num_curve_points):
                y, x = unpack('!hh', acv_file.read(4))
                curve.append((x, y))
            curves.append(curve)

        return curves

    def _find_coefficients(self):
        polynomials = []
        for curve in self.curves:
            xdata = [x[0] for x in curve]
            ydata = [x[1] for x in curve]
            p = interpolate.lagrange(xdata, ydata)
            polynomials.append(p)
        return polynomials

    def get_r(self):
        return self.polynomials[1]

    def get_g(self):
        return self.polynomials[2]

    def get_b(self):
        return self.polynomials[3]

    def get_c(self):
        return self.polynomials[0]


class FilterManager:

    def __init__(self):
        self.filters = {}
        # add some stuff here

    def add_filter(self, filter_obj):
        # Overwrites if such a filter already exists
        # NOTE: Fix or not to fix?
        self.filters[filter_obj.name] = filter_obj

    def apply_filter(self, filter_name, image_array):

        if image_array.ndim < 3:
            raise Exception('Photos must be in color, meaning at least 3 channels')
        else:
            def interpolate(i_arr, f_arr, p, p_c):
                p_arr = p_c(f_arr)
                return p_arr

                # NOTE: Assumes that image_array is a numpy array

            image_filter = self.filters[filter_name]
            # NOTE: What happens if filter does not exist?
            width, height, channels = image_array.shape
            filter_array = numpy.zeros((width, height, 3), dtype=float)

            p_r = image_filter.get_r()
            p_g = image_filter.get_g()
            p_b = image_filter.get_b()
            p_c = image_filter.get_c()

            filter_array[:, :, 0] = p_r(image_array[:, :, 0])
            filter_array[:, :, 1] = p_g(image_array[:, :, 1])
            filter_array[:, :, 2] = p_b(image_array[:, :, 2])
            filter_array = filter_array.clip(0, 255)
            filter_array = p_c(filter_array)

            filter_array = numpy.ceil(filter_array).clip(0, 255)

            return filter_array.astype(numpy.uint8)


def add_curve(img, curve_path):
    img_filter = Filter(curve_path, 'crgb')

    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    image_array = numpy.array(im)

    filter_manager = FilterManager()
    filter_manager.add_filter(img_filter)

    filter_array = filter_manager.apply_filter('crgb', image_array)
    im = Image.fromarray(filter_array)
    ret_img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
    return ret_img


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Wrong number of arguments")
        print("""  Usage: \
          python filter.py [curvefile] [imagefile] """)
    else:
        img_filter = Filter(sys.argv[1], 'crgb')

        im = Image.open(sys.argv[2])

        im.show()

        image_array = numpy.array(im)

        filter_manager = FilterManager()
        filter_manager.add_filter(img_filter)

        filter_array = filter_manager.apply_filter('crgb', image_array)
        im = Image.fromarray(filter_array)
        im.save('temp.png')
        im.show()
