"""
MATRIX BUILDER

Builds matrices for all the filters that need to extract information from all the
other different files.

SYSTEM

in function extract, you specify what values to extract.
there is a code to specify what you want to extract

the order that the values come specifies what order the values are in

"""
import numpy as np
from yaml import load


reference = './resources/data_sources.yaml'


"""
CLASS + SUBCLASS + ITEM
 (H)      (G)       (x)

example:
3
extract('data-1', 'HA', 'TGx', 'TGy', 'M')

"""


def extract(filename, *argv):
    """
    :param filename:
    :param argv:
    :return:
    """
    yamlfile = load(open('./resources/data_sources.yaml', 'r'))

    result = []

    # iterating through arguments
    for arg in argv:
        # ex: HAx
        # load file
        indices = []  # all items to retrieve

        # print('class: {}'.format(arg[0]))
        # print('file path: {}'.format(yamlfile[arg[0]]['file_path']))

        if len(arg) == 1:
            # select the entire range
            # print('range: {}'.format(yamlfile[arg[0]]['range']))
            indices = yamlfile[arg[0]]['range']

        if len(arg) == 2:
            # select the subclass range
            # print('subclass: {}'.format(arg[1]))
            # print('range: {}'.format(yamlfile[arg[0]][arg[1]]['range']))
            indices = yamlfile[arg[0]][arg[1]]['range']

        if len(arg) == 3:
            # select selector location
            # print('subclass: {}'.format(arg[1]))
            # print('selector: {}'.format(arg[2]))
            # print('location: {}'.format(yamlfile[arg[0]][arg[1]][arg[2]]))
            indices = yamlfile[arg[0]][arg[1]][arg[2]]

        # print()
        # print(indices)

        # initializing result values
        if len(indices) == 1:
            # just a location
            values = [[]]
        else:
            # a range of values
            values = [[] for i in range(indices[0], indices[1])]

        # print(values)
        # print()

        #################
        # Enter in Data #
        #################
        datafile = None

        try:
            # open the raw file, lowpass file, etc
            datafile = open('{}/{}'.format(filename, yamlfile[arg[0]]['file_path']))
            # extract all values and put in matrix
            if len(indices) == 1:
                # just one location
                for line in datafile:
                    values[0].append(float(line.split(sep=' ')[indices[0]]))

            else:
                # range of locations
                for row in datafile:
                    line = row.split(sep=' ')
                    for i in range(0, indices[1] - indices[0]):
                        values[i].append(float(line[i+indices[0]]))

            # add on lists
            result.extend(values)

        finally:
            datafile.close()

    # print(np.matrix(result))
    # return np.matrix(result)
    return result
