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
    Generates a RoseDiagram to show direction data

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

    Returns
    -------
    The created RoseDiagram object containing a rose diagram.

    """
    
    rose = RoseDiagram(data, **kargs )
    rose.show()
    
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
        
        TODO: make the options accessible

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

        if self.data is None:
            if self.verbose: print("Undefined dataset, not drawing.")
        else:
            if self.verbose: print("Plotting the diagram")
            # using seaborn for drawing the polar histogram
            sns_ax = sns.histplot(self.data, x= self.direction_label_rad, hue= self.category_label,
                 binwidth= self.bin_width_rad, binrange= [-self.bin_width_rad/2.0,2*np.pi],
                 stat= "count", # count, percent, frequency, proportion, density
                 #hue_order = ["Rand", "Fam1","Fam2"],
                 multiple="layer", # {“layer” or "stack", the others produce strange results “dodge”, “fill”}
                 element= "bars", # {“bars”,  the others produce strange results  “step”, “poly”}
                 edgecolor="k", linewidth=0.75, zorder= 10,
                 palette= "bright", # deep, colorblind, bright, muted, dark, pastel
                 ax= self.ax, legend= True )
            if self.category_label is not None:
                sns.move_legend(sns_ax, "upper left", bbox_to_anchor = (1.1, 1))
        
        r_ticks = self.ax.get_yticks()
        self.ax.set_rgrids( r_ticks, angle=0)
        self.ax.set_ylabel("")

        

