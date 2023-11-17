import numpy as np
from tutils import BaseStateSystem
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from typing import Tuple


def random_initialiser(shape: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
    """Initializes two arrays with random values."""
    return (
        np.random.normal(loc=0, scale=0.05, size=shape),
        np.random.normal(loc=0, scale=0.05, size=shape),
    )


class TwoDimensionalRDEquations(BaseStateSystem):
    """Class for solving two-dimensional reaction-diffusion equations."""

    def __init__(
        self,
        Da: float,
        Db: float,
        Ra: callable,
        Rb: callable,
        initialiser: callable = random_initialiser,
        width: int = 1000,
        height: int = 1000,
        dx: float = 1,
        dt: float = 0.1,
        steps: int = 1,
    ):
        """Initializes the TwoDimensionalRDEquations object.

        Args:
            Da: Diffusion coefficient for component A.
            Db: Diffusion coefficient for component B.
            Ra: Reaction function for component A.
            Rb: Reaction function for component B.
            initialiser: Function to initialize the state arrays.
            width: Width of the simulation grid.
            height: Height of the simulation grid.
            dx: Spatial step size.
            dt: Time step size.
            steps: Number of steps to update in each iteration.
        """
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.initialiser = initialiser
        self.width = width
        self.height = height
        self.shape = (width, height)
        self.dx = dx
        self.dt = dt
        self.steps = steps
        self.laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]) / (dx**2)

    def initialise(self):
        """Initializes the state arrays for the simulation."""
        self.t = 0
        self.a, self.b = self.initialiser(self.shape)

    def update(self):
        """Updates the state of the system for a specified number of steps."""
        for _ in range(self.steps):
            self.t += self.dt
            self._update()

    def _update(self):
        """Performs a single update step."""
        La = convolve(self.a, self.laplacian_kernel, mode="wrap")
        Lb = convolve(self.b, self.laplacian_kernel, mode="wrap")
        np.add(self.a, self.dt * (self.Da * La + self.Ra(self.a, self.b)), out=self.a)
        np.add(self.b, self.dt * (self.Db * Lb + self.Rb(self.a, self.b)), out=self.b)

    def draw(self, ax):
        for axis in ax:
            axis.clear()
            axis.grid(visible=False)
            axis.axis("off")

        ax[0].imshow(self.a, cmap="jet")
        ax[1].imshow(self.b, cmap="brg")

    def initialise_figure(self):
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        return fig, ax
