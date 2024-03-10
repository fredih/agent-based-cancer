from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement

class MultipleCanvasGrid(VisualizationElement):
    """MESA's modified CanvasGrid to allow fow having multiple secondary sites

    Works both in batch and live rendering
    
    A CanvasGrid object uses a user-provided portrayal method to generate a
    portrayal for each object. A portrayal is a JSON-ready dictionary which
    tells the relevant JavaScript code (GridDraw.js) where to draw what shape.

    The render method returns a dictionary, keyed on layers, with values as
    lists of portrayals to draw. Portrayals themselves are generated by the
    user-provided portrayal_method, which accepts an object as an input and
    produces a portrayal of it.

    A portrayal as a dictionary with the following structure:
        "x", "y": Coordinates for the cell in which the object is placed.
        "Shape": Can be either "circle", "rect", "arrowHead" or a custom image.
            For Circles:
                "r": The radius, defined as a fraction of cell size. r=1 will
                     fill the entire cell.
                "xAlign", "yAlign": Alignment of the circle within the cell.
                                    Defaults to 0.5 (center).
            For Rectangles:
                "w", "h": The width and height of the rectangle, which are in
                          fractions of cell width and height.
                "xAlign", "yAlign": Alignment of the rectangle within the
                                    cell. Defaults to 0.5 (center).
            For arrowHead:
                "scale": Proportion scaling as a fraction of cell size.
                "heading_x": represents x direction unit vector.
                "heading_y": represents y direction unit vector.
             For an image:
                The image must be placed in the same directory from which the
                server is launched. An image has the attributes "x", "y",
                "scale", "text" and "text_color".
        "Color": The color to draw the shape in; needs to be a valid HTML
                 color, e.g."Red" or "#AA08F8"
        "Filled": either "true" or "false", and determines whether the shape is
                  filled or not.
        "Layer": Layer number of 0 or above; higher-numbered layers are drawn
                 above lower-numbered layers.
        "text": The text to be inscribed inside the Shape. Normally useful for
                showing the unique_id of the agent.
        "text_color": The color to draw the inscribed text. Should be given in
                      conjunction of "text" property.


    Attributes:
        portrayal_method: Function which generates portrayals from objects, as
                          described above.
        grid_height, grid_width: Size of the grid to visualize, in cells.
        canvas_height, canvas_width: Size, in pixels, of the grid visualization
                                     to draw on the client.
        template: "canvas_module.html" stores the module's HTML template.

    """

    package_includes = ["GridDraw.js", "CanvasModule.js", "InteractionHandler.js"]

    def __init__(
        self,
        portrayal_method,
        grid_width,
        grid_height,
        canvas_width=500,
        canvas_height=500,
        site=0
    ):
        """Instantiate a new CanvasGrid.

        Args:
            portrayal_method: function to convert each object on the grid to
                              a portrayal, as described above.
            grid_width, grid_height: Size of the grid, in cells.
            canvas_height, canvas_width: Size of the canvas to draw in the
                                         client, in pixels. (default: 500x500)

        """
        self.portrayal_method = portrayal_method
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.site = site
        new_element = "new CanvasModule({}, {}, {}, {})".format(
            self.canvas_width, self.canvas_height, self.grid_width, self.grid_height
        )

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        model.grid=model.grids[self.site]
        grid_state = defaultdict(list)
        for x in range(model.grids[self.site].width):
            for y in range(model.grids[self.site].height):
                cell_objects = model.grids[self.site].get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    portrayal = self.portrayal_method(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state