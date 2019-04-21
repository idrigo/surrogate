import numpy as np
import cfg
try:
    from src.netcdftools import MyNetCDF  # for classical usage
except:
    from netcdftools import MyNetCDF # for Jupyter Notebook


class FeatureTable:

    def __init__(self, data, x, y, t=0, dx=0, dy=0, dt=0):

        self.data = data
        self.selection = None
        self.point = [t, x, y]

        self.dx = dx
        self.dy = dy
        self.dt = dt

        self.matrix = None

    def field_idx(self):

        deltas = [self.dt, self.dx, self.dy]
        assert len(self.point) == len(deltas), 'coordinates and deltas should be same lenght'
        d = []
        for i, c in enumerate(self.point):
            start = c - deltas[i]
            stop = c + deltas[i] + 1
            l = list(range(start, stop))
            d.append(l)

        mesh = np.meshgrid(*d)
        out = []
        for arr in mesh:
            out.append(arr.ravel())

        idx = np.column_stack([*out])

        datashape = np.shape(self.data)
        # sel = (idx >= 0).all(axis=1)

        idx = idx[(idx[:, 0] >= 0) & (idx[:, 0] < datashape[0])
                  & (idx[:, 1] >= 0) & (idx[:, 1] < datashape[1])
                  & (idx[:, 2] >= 0) & (idx[:, 2] < datashape[2])]
        return idx

    def select(self):
        selection = []
        indexes = self.field_idx

        for i, val in enumerate(indexes):
            ix = tuple(indexes[i])
            selection.append(self.data[ix])

        self.selection = np.array(selection)
        return self.selection

    def gen_matrix(self):
        matrix = []
        for i in range(np.shape(self.data)[0]):
            self.point[0] = i
            selection = self.select()
            matrix.append(selection)

        self.matrix = np.array(matrix)

        return self.matrix
