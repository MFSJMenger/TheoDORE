from theodore import theo_header, lib_file
import numpy
import os

from colt import Colt, from_commandline


try:
    import matplotlib
    matplotlib.use('Agg')
    import pylab
except:
    print("pylab/matplotlib not installed - plotting not possible")
    raise


@from_commandline("""
fname = OmFrag.txt :: existing_file
""")
def read_om_frag(fname='OmFrag.txt'):
    """
    Read the OmFrag.txt file written by analyze_tden.py
    """
    state_list = []
    maxOm = 0.0
    with open(fname, 'r') as Ofile:
        line = next(Ofile)
        numF = int(line)
        while True:
            line = next(Ofile, None)
            if line is None:
                break

            words = line.split()

            state = {}
            state_list.append(state)

            state['name'] = words[0]
            state['Om'] = words[1]
            state['OmFrag'] = numpy.zeros([numF, numF])

            for iel, el in enumerate(words[2:]):
                iF = iel %  numF
                jF = iel // numF
                state['OmFrag'][iF, jF] = el

            maxOm = max(maxOm, state['OmFrag'].max())
        return state_list, maxOm


class OmFrag_options(Colt):
    """
    Set and store the options for plotting.
    """
    _questions = """
    # Scale the values before plotting?
    scaled = no :: str :: [no, squareroot]

    # Resolution (dpi) for plotting (plot_dpi):
    plot_dpi = 200 :: int

    # Coloring scheme for pseudocolor plots (cmap):
    #       Greys - Grey scale
    #     Oranges - Orange scale
    #       Blues - Blue scale
    #        RdBu - Red -> Blue
    #        YlGn - Yellow -> Green
    #      YlOrRd - Yellow -> Orange -> Red
    #      YlOrBr - Yellow -> Orange -> Brown
    #      RdYlBu - Red -> Yellow -> Blue
    #      binary - White -> Black
    #      bone_r - White -> Blue -> Black
    #      pink_r - White -> Pink -> Black
    #       hot_r - White -> Yellow -> Red -> Black
    color_map = Greys :: str :: [Greys, Oranges, Blues, RdBu, YlGn, YlOrRd, RdYlBu, binary, bone_r, pink_r, hot_r]

    # Font size (fsize):
    font_size = 10 :: int

    # Format of output graphics files (output_format):
    output_format = png

    # Use the same scale for all plots (sscale):
    same_scale = yes :: bool

    # Minimal value to plot (vmin):
    vmin = 0.00

    # Maximal value to plot (vmax):
    vmax = :: float, optional

    # Plot frame? (axis):
    plot_axis = yes :: bool

    # Axis with tick labels? (ticks):
    show_ticks = yes :: bool

    # Draw grid? (grid):
    draw_grid = yes :: bool

    # Plot colorbar for each individual plot? (cbar):
    cbar = no :: bool
    """

    def from_config(cls, config, state_list, maxOm):
        return cls(config, state_list, maxOm)

    def __init__(self, settings, state_list, maxOm):
        self.state_list = state_list
        self.settings = settings
        if settings['vmax'] is not None:
            self.maxOm = settings['vmax']
        else:
            self.maxOm = maxOm

    def plot(self):
        hfname = 'OmFrag.html'
        hfile = lib_file.htmlfile(hfname)
        hfile.pre('Electron-hole correlation plots')
        hfile.write('<h2>Electron-hole correlation plots of the Omega matrices for the individual states.</h2>')

        htable = lib_file.htmltable(ncol=4)

        matplotlib.rc('font', size=self.settings['font_size'])

        if self.settings['draw_grid'] is True:
            edgecolors='k'
        else:
            edgecolors=None

        for state in self.state_list:
            if self.settings['scaled'] == 'no':
                plot_arr = state['OmFrag']
            elif self.settings['scaled'] == 'squareroot':
                plot_arr = numpy.sqrt(state['OmFrag'])

            if self.settings['same_scale'] is True:
                vmin = self.settings['vmin']
                vmax = self.maxOm
            else:
                vmin = 0.
                vmax = state['OmFrag'].max()

            # Completely delete the small elements
            # for x in numpy.nditer(plot_arr, op_flags = ['readwrite']):
            #     if x < vmin:
            #         x[...] = -1. # numpy.nan

            pylab.figure(figsize=(2,2))
            pylab.pcolor(plot_arr, cmap=pylab.get_cmap(name=self.settings['color_map']), vmin=vmin, vmax=vmax, edgecolors=edgecolors)

            # *** Different colouring of different parts ***
            # frag_lists = [[0, 2, 4, 6], [1, 3, 5]]
            # cmaps = ['Reds', 'Blues']
            # OmDim = len(plot_arr)
            # for frag in frag_lists:
            #     tmp_arr = numpy.array([[numpy.nan for i in range(OmDim)] for j in range(OmDim)])
            #     for i in frag:
            #         tmp_arr[i,i] = plot_arr[i,i]
            #     pylab.pcolor(tmp_arr, cmap=pylab.get_cmap(cmaps.pop(0)), vmin=0., vmax=vmax, edgecolors=edgecolors)

            if self.settings['plot_axis']:
                pylab.axis('on')
                if self.settings['show_ticks']:
                    pylab.tick_params(which='both', length=0)
                    #if self.settings['show_ticks'] is True:
                    if False:
                        pylab.xticks([x + 0.5 for x in range(len(plot_arr))], self['xticks'])
                        pylab.yticks([y + 0.5 for y in range(len(plot_arr))], self['yticks'])
                    else:
                        pylab.xticks([x + 0.5 for x in range(len(plot_arr))], [x + 1 for x in range(len(plot_arr))])
                        pylab.yticks([y + 0.5 for y in range(len(plot_arr))], [y + 1 for y in range(len(plot_arr))])
                else:
                    pylab.xticks([])
                    pylab.yticks([])
            else:
                pylab.axis('off')

            if self.settings['cbar'] is True:
                pylab.colorbar()

            pname = 'pcolor_%s.%s'%(state['name'], self.settings['output_format'])
            print("Writing %s ..."%pname)
            pylab.tight_layout()
            pylab.savefig(pname, dpi=self.settings['plot_dpi'])
            pylab.close()

            tel  = '<img src="%s", border="1" width="200">\n'%pname
            tel += '<br>%s'%state['name']
            htable.add_el(tel)

        # create a plot with the e/h axes and optionally the scale
        pylab.figure(figsize=(3,2))
        matplotlib.rc('font', size=14)
        ax = pylab.axes()
        ax.arrow(0.15, 0.15, 0.5, 0., head_width=0.05, head_length=0.1, fc='r', ec='r')
        ax.text(0.20, 0.03, 'hole', color='r')
        ax.arrow(0.15, 0.15, 0., 0.5, head_width=0.05, head_length=0.1, fc='b', ec='b')
        ax.text(0.02, 0.20, 'electron', rotation='vertical', color='b')

        pylab.axis('off')
        if self.settings['same_scale']:
            pylab.savefig('axes_no.%s'%self.settings['output_format'], dpi=self.settings['plot_dpi'])
#            pylab.figure(figsize=(2,2))

            pylab.pcolor(numpy.zeros([1, 1]), cmap=pylab.get_cmap(name=self.settings['color_map']), vmin=self.settings['vmin'], vmax=self.maxOm)

            pylab.colorbar()

        pylab.savefig('axes.%s'%self.settings['output_format'], dpi=self.settings['plot_dpi'])

        tel  = '<img src="axes.%s", border="1" width="200">\n'%self.settings['output_format']
        tel += '<br>Axes / Scale'
        htable.add_el(tel)

        hfile.write(htable.ret_table())
        hfile.post()

        print(" HTML file %s containing the electron-hole correlation plots written."%hfname)

def run_plot():
    # read data from commandline
    state_list, maxOm = read_om_frag()
    Oopt = OmFrag_options.from_questions(state_list, maxOm, config='plot_OmFrag.in')
    Oopt.plot()


if __name__ == '__main__':
    theo_header.print_header('Plot Omega matrices')
    run_plot()
