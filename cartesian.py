import math



class Point:
    def __init__(self, x_px: int, y_px: int, width: int, height: int) -> None:
        '''
        Creates a point with coordinates stored as fractional distances
        across a given width and height.
        '''
        self._fract_x = x_px/width
        self._fract_y = y_px/height

    def fract_coord(self) -> (float):
        '''
        Returns a tuple of the coordinates in fractional form.
        '''
        return (self._fract_x, self._fract_y)

    def px_coord(self, width: int, height: int) -> (int):
        '''
        Returns a tuple of the coordinates in pixel form.
        The user must give the current dimensions of the 2D
        area.
        '''
        return (int(self._fract_x*width), int(self._fract_y*height))

    def equals(self, other_point: "Point") -> bool:
        '''
        Compares this point with another point.
        Considers them equivalent if their x and y fractional
        coordinates are equal.
        '''
        other_point_coord = other_point.fract_coord()

        if self._fract_x == other_point_coord[0] \
           and self._fract_y == other_point_coord[1]:
            return True
        else:
            return False


class Circle:
    def __init__(self, p1: "Point", p2: "Point", color: str) -> None:
        '''
        Creates a circle/oval with two opposite corner points representing
        those of a square/rectangle just large enough to hold the circle.
        Also assigns a specified color to the circle.
        '''
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def get_color(self) -> str:
        '''
        Allows the user to change the color.
        '''
        return self.color

    def get_points(self) -> ("Point"):
        '''
        Returns the two points representing the opposite corners of
        the containing square.
        '''
        return (self.p1, self.p2)

    def equals(self, other_circle: "Circle") -> bool:
        '''
        Compares this circle with another and considers
        them equivalent if their pairs of corner points are
        equivalent.
        '''
        other_circle_points = other_circle.get_points()

        if (other_circle_points[0].equals(self.p1) and \
           other_circle_points[1].equals(self.p2)) or \
           (other_circle_points[1].equals(self.p1) and \
           other_circle_points[0].equals(self.p2)):
            return True
        else:
            return False


class Rectangle:
    def __init__(self, p1: "Point", p2: "Point") -> None:
        '''
        Creates a rectangle withe two opposite corner points.
        Assigns it default fill and border colors.
        '''
        self.p1 = p1
        self.p2 = p2
        self.color = '#EDE6B7'
        self.border_color = 'black'

    def get_points(self) -> ("Points"):
        '''
        Returns the two opposite cornor points of the rectangle.
        '''
        return (self.p1, self.p2)

    def get_color(self) -> str:
        '''
        Returns the fill color.
        '''
        return self.color

    def get_border_color(self) -> str:
        '''
        Returns the border color.
        '''
        return self.border_color

    def contains(self, point: "Point") -> bool:
        '''
        Given a point, this will see if the rectangle contains
        the point.
        '''
        p1_coord = self.p1.fract_coord()
        p2_coord = self.p2.fract_coord()
        point_coord = point.fract_coord()

        if ((point_coord[0] > p1_coord[0] and point_coord[0] < p2_coord[0]) \
            or (point_coord[0] < p1_coord[0] and point_coord[0] > p2_coord[0])) \
            and ((point_coord[1] > p1_coord[1] and point_coord[1] < p2_coord[1]) \
            or (point_coord[1] < p1_coord[1] and point_coord[1] > p2_coord[1])):

            return True

        else:
            return False


class CircleState:
    def __init__(self) -> None:
        '''
        Keeps a list of all the circles in existence.
        '''
        self.circles = []

    def all_circles(self) -> ["Circle"]:
        '''
        Returns a list of all the existing circles.
        '''
        return self.circles

    def append_circle(self, new_circle: "Circle") -> None:
        '''
        Adds a new circle to the list of circles in existence.
        '''
        self.circles.append(new_circle)

    def remove_circle(self, unwanted_circle: "Circle") -> None:
        '''
        Takes a circle and removes any equivalent circles from
        the list of circles in existence.
        '''
        for circle in self.circles:
            if circle.equals(unwanted_circle):
                circles.remove(circle)


class RectangleState:
    def __init__(self) -> None:
        '''
        Keeps a list of all the rectangles in existence.
        '''
        self.rectangles = []

    def append_rect(self, new_rect: "Rectangle") -> None:
        '''
        Adds a new rectangle to the list of rectangles in existence.
        '''        
        self.rectangles.append(new_rect)

    def all_rects(self) -> ["Rectangle"]:
        '''
        Returns a list of all the rectangles in existence.
        '''
        return self.rectangles



def index_to_grid_coord(index: int, no_of_rows: int, no_of_col: int) -> (int):
    '''
    Converts a list index into its equivalent coordinates which it would
    have if the list gets divided into rows which get stacked atop each
    other to form a grid. The grid coordinates are assumed to start at 0.
    '''
    row_index = (index + 1)/no_of_col

    if row_index % 1 != 0:
        row_index = math.floor(row_index)
    else:
        row_index = row_index - 1

    col_index = index % no_of_col

    return (int(col_index), int(row_index))


def grid_coord_to_index(row_index: int, col_index: int, no_of_col: int) -> int:
    '''
    Converts the coordinates of cells in a grid to the
    index which the cell would have if the the rows of
    the grid were added into a list. The grid coordinates
    are assumed to start at 0.
    '''
    index = row_index * no_of_col
    index = index + col_index
    return index

