# -*- coding: utf-8 -*-
"""geoplot module from the GeoDataKit: tools for ploting geoscience diagrams

This module mainly relies on advanced ploting libraries, which are called
in specific ways to produce scientific visualisation tailored to geoscience
needs. Datasets are also prepared and processed for making the diagram 
generation easier.

The libraries used here are:
    - matplotlib: this library is used as a backend for others (e.g., seaborn)
    or directly to develop new visualisation tools
    - seaborn: this specialised visualisation library for statistical views
    is the main entry point for static diagrams
    - plotly: this library based on top of plotly.js uses javascript for
    runing interactive plots in HTML based enviromnent. It is used when helpful
    to visualise interactive plots.

The implemented plots are defined in classes:
    - RoseDiagram: builds a plot for showing direction distributions
    
Helper functions provide direct access to the diagram generation:
    - rose_diagram(): generates a RoseDiagram
"""

from GeoDataKit.utils import get_kargs

import numbers
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

def rose_diagram(data, **kargs):
    """
    Generates a RoseDiagram to show direction data.

    Parameters
    ----------
    data : :class:`pandas.DataFrame` or array-like data
        the dataset containing the direction data. Either passed as a DataFrame
        or as an array-like structure. If an array-like structure is used, then
        it must be passed as a single column array containing only the 
        direction data. If a DataFrame is used, the column containing the 
        directions must be specified by setting the column name in the 
        direction parameter. If using a DataFrame, optionally, a category
        can be associated with each entry. It must be described by another
        column in the DataFrame containing a string or integer corresponding to
        the classification; in this case, category parameter must receive the
        name of the corresponding column.
    **kargs: dict()
        keyword arguments passed to the `RoseDiagram` methods. Refer to the 
        documentation of this class to see the full list of arguments.
        
        
    Keyword arguments
    ---------------
    direction_label : str, optional
        Label of the column containing the direction data. Must be given if the
        dataset is passed as a DataFrame. The default is None.
    category_label : str, optional
        Label of the column containing a classification of the entries in the
        dataset. The default is None.
    degrees: bool, optional
        tells whether the data is in degrees or in radian.
        Default is True, meaning it is in degrees.
    bin_width: float, optional
        The width of the histogram bars in degrees if degrees is True,
        in radian otherwise. Default is 10.
    verbose: bool, optional
        Specify the behaviour of the class, whether it should
        output information or not. The default is False.

    Returns
    -------
    The created RoseDiagram object containing a rose diagram.

    """
    
    rose = RoseDiagram(data, **kargs )
    rose.show(**kargs)
    
    return rose

class RoseDiagram:
    """RoseDiagram: a polar histogram to analyse directional data
    
    A Rose diagram is a special kind of graphics used in geosciences
    for depicting the distribution of directions in a dataset.
    It is called Rose as a reference to the flower-like shape of the diagram.
    
    In this representation, the directions are separated into bins of small
    ranges of equal width and the number (or proportion) of entries falling 
    into each bin is represented by the length of a bar oriented in the 
    corresponding direction. This is very much like an histogram in polar
    coordinates. Each bar looks like a petal in a rose.
        
    Attributes
    -----------
    data: :class:`pandas.DataFrame`
        A Pandas DataFrame containing the direction dataset and categories
        if necessary.
    fig: Figure
        A Matplotlib Figure in which the diagram is drawn.
    ax: Axes
        A Matplotlib Axes in which the diagram is plotted
    
    Methods
    -----------
    set_data()
        set or updates the dataset
    show()
        Plots the Rose diagram
    """
    
    def __init__(self, data= None, **kargs ):
        """
        Constructor of a RoseDiagram.
        
        Parameters
        ----------
        data: :class:`pandas.DataFrame`, optional
            the dataset containing the orientation data.
            Orientation is expected to be expressed in degrees clockwise from
            North direction. The default is None as the data could be set later
            on by calling set_data().
            
        Keyword arguments
        ---------------
        direction_label : str, optional
            Label of the column containing the direction data. Must be given if the
            dataset is passed as a DataFrame. The default is None.
        category_label : str, optional
            Label of the column containing a classification of the entries in the
            dataset. The default is None.
        degrees: bool, optional
            tells whether the data is in degrees or in radian.
            Default is True, meaning it is in degrees.
        bin_width: float, optional
            The width of the histogram bars in degrees if degrees is True,
            in radian otherwise. Default is 10.
        verbose: bool, optional
            Specify the behaviour of the class, whether it should
            output information or not. The default is False.

        Returns
        -------
        None.

        """
        
        self.verbose = get_kargs("verbose", False, **kargs)
        if self.verbose: print("Preparing the data")
        
        degrees= get_kargs("degrees", True, **kargs)
        bin_width= get_kargs("bin_width", 10, **kargs)
        
        self.bin_width_rad = np.deg2rad(bin_width) if degrees else bin_width
        
        self.set_data(data, **kargs)
        
    def set_data(self, data, **kargs ):
        """
        Setter of dataset
        
        Parameters
        ----------
        data: :class:`pandas.DataFrame` 
            the dataset containing the orientation data.
            Orientation is expected to be expressed in degrees clockwise from
            North direction.
        direction_label : str, optional
            Label of the column containing the direction data. Must be given if
            the dataset is passed as a DataFrame. The default is None, if so 
            the first column with values is used.
        category_label : str, optional
            Label of the column containing a classification of the entries in the
            dataset. The default is None.
        degrees: bool
            tells whether the data is in degrees or in radian.
            Default is True, meaning it is in degrees.

        Returns
        -------
        None.

        """
        
        
        # processing the data
        if data is None:
            if self.verbose and (self.data is not None): print("Resetting the dataset.")
            self.data = data
            return
        assert( isinstance(data, pd.DataFrame)), "data must be a pd.DataFrame. Here data was: "+type(data)
        self.data = data
        
        # finding the direction label (either given or first value column)
        self.direction_label= get_kargs("direction_label", None, **kargs)
        assert(not self.data.empty), "data must contain values, here data.empty is True"
        number_columns = [col for col in self.data.columns if isinstance(self.data[col].iloc[0], numbers.Number) ]
        assert(len(number_columns)>0), "data must contain at least one column with numbers, here none was found in data:\n"+str(self.data.head())
        self.direction_label = number_columns[0]
        
        self.category_label = get_kargs("category_label", None, **kargs)
        degrees= get_kargs("degrees", True, **kargs)
        
        # converting data from degrees to rad
        self.direction_label_rad = self.direction_label+"_rad" \
                                    if degrees and (self.direction_label is not None) \
                                    else self.direction_label
        if degrees and (self.data is not None):
            self.data[self.direction_label_rad] = np.deg2rad(self.data[self.direction_label]) 
        
    def show(self, **kargs):
        """
        Plots the Rose diagram.
        
        Parameters
        -----------
        stat_type: str, optional
            specifies which kind of statistics should be used for the bars:
                count, percent, frequency, proportion, density.
                Default is count. The options are copied from seaborn:
            - `count`: show the number of observations in each bin
            - `frequency`: show the number of observations divided by the bin width
            - `probability`: or `proportion`: normalize such that bar heights sum to 1
            - `percent`: normalize such that bar heights sum to 100
            - `density`: normalize such that the total area of the histogram equals 1
        x_axis_label: str, optional
            specifies the label for the orientation (theta) axis. Default is
            the name of the column containing the orientation data.
        y_axis_label: str, optional
            specifies the label for the statistics (r) axis. Default is
            the text specified by default depending on the choice of stat_type.
            Use None to remove te label.
        y_axis_label_padding: int, optional
            padding to shift the location of the y axis label and avoid 
            intersection with the orientation labels. Default is 20.
        y_axis_angle: number, optional
            the location of the y_axis values, as an angle in degree. Default 0
        category_order: list, optional
            specifies the ordering of the categories to be plotted. The first 
            one is on top of the other and so on. Should give a list of 
            category namesDefault is None, i.e., keeps the default ordering.
        bin_shape: str, optional
            specifies the shape of the bins. Default is bars.
            -`bars`: each bin is an individual bar
            -`step`: all the bars in each category are gathered in a same shape
            -`poly`: a polygone is drawn for each category, producing a 
            smoother shape.
        category_interaction: str, optional
            specifies how different category should interact. Default `layer`
            - `layer`: each category is drawn in a different layer, visible by 
            transparency below those above.
            - `stack`: each category is drawn in the continuation of the 
            previous shape, stacking it in the radial direction.
            - `proportion`: the drawing will fill all the radial space and
            the proportion of each category is represented by the relative
            portion of the shape occupied by the category.
        edge_color: str, optional
            a matplolib color or string to specify the color of the edges of 
            the shapes.
        edge_width: float, optional
            the thickness of the shape edges. Use 0. to remove the edges.
            Default is 0.75
        color_palette: str; optional
            variations of the color palette to be used for categories. cf.,
            seaborn documentation:  deep, colorblind, bright, muted, dark,
            pastel. Default is bright.
        alpha: float, optional
            set the level of transparency. Default is 0.75.
        shrink: float, optional
            shrinking makes the bars smaller in width which better separates
            the bars for visualisation purpose. It is given as a factor of 
            contraction (shrink) between 1 (full width) and 0 (completely 
            collapsed). It only affects the "bars" layout (i.e., ignored for
            "step" and "poly". Default is 1. (i.e., no shrink).

        Returns
        -------
        None.

        """
        
        if self.verbose: print("Creating the diagram")
        self.fig = plt.figure()
        self.fig.set_size_inches((14,8))
        self.ax = plt.axes(projection= "polar")
        # setting the theta orientation properly
        self.ax.set_theta_zero_location('N') # set the North up
        self.ax.set_theta_direction(-1) # set the angles clock-wise
        # add grid every 10 degree and North East South West main directions
        self.ax.set_thetagrids(angles=np.concatenate((np.arange(0, 360, 10), np.arange(0, 360, 90))),
                          labels=np.concatenate((np.arange(0, 360, 10), ["N","E","S","W"])))

        # parameters
        stat_type = get_kargs("stat_type","count",**kargs)
        bin_shape = get_kargs("bin_shape","bars",**kargs)
        category_order = get_kargs("category_order",None,**kargs)
        category_interaction = get_kargs("category_interaction","layer",**kargs)
        category_interaction = "fill" if category_interaction == "proportion" else category_interaction
        x_axis_label = get_kargs("x_axis_label",self.direction_label, **kargs)
        y_axis_label = get_kargs("y_axis_label","default", **kargs)
        y_axis_label_padding = get_kargs("y_axis_label_padding",20, **kargs)
        y_axis_angle = get_kargs("y_axis_angle",0, **kargs)
        edge_color = get_kargs("edge_color","k", **kargs)
        edge_width = get_kargs("edge_width",0.75, **kargs)
        color_palette = get_kargs("color_palette","bright", **kargs)
        alpha = get_kargs("alpha",0.75, **kargs)
        shrink = get_kargs("shrink",1.0, **kargs)

        if self.data is None:
            if self.verbose: print("Undefined dataset, not drawing.")
        else:
            if self.verbose: print("Plotting the diagram")
            # using seaborn for drawing the polar histogram
            sns_ax = sns.histplot(self.data, x= self.direction_label_rad, hue= self.category_label,
                 binwidth= self.bin_width_rad, binrange= [-self.bin_width_rad/2.0,2*np.pi],
                 stat= stat_type,
                 hue_order= category_order,
                 multiple= category_interaction,
                 element= bin_shape,
                 edgecolor= edge_color, linewidth= edge_width, zorder= 10,
                 palette= color_palette,
                 alpha= alpha,
                 shrink= shrink,
                 ax= self.ax, legend= True )
            if self.category_label is not None:
                sns.move_legend(sns_ax, "upper left", bbox_to_anchor = (1.1, 1))
        
        r_ticks = self.ax.get_yticks()
        self.ax.set_rgrids( r_ticks, angle= y_axis_angle)
        if y_axis_label != "default":
            self.ax.set_ylabel(y_axis_label)
        self.ax.set_ylabel(self.ax.get_ylabel(),labelpad= y_axis_label_padding)
        self.ax.set_xlabel(x_axis_label)


# script usage
if (__name__ == '__main__'):
    import GeoDataKit.dataset as dataset
    data = dataset.get_dataset("orientation")
    rose_diagram(data, category_label="category", bin_width=20,
                 color_palette= "bright",
                 category_order= ["Rand","Cat1","Cat2"],
                 stat_type= "density",
                 x_axis_label= "Orientation (°)")

