from diffusion import TwoDimensionalRDEquations
import click
import numpy as np

WIDTH = 200
HEIGHT = 200
DX = 1
DT = 0.001


@click.command()
@click.option("--da", default=1.0, type=float, help="Diffusion coefficient for A.")
@click.option("--db", default=100.0, type=float, help="Diffusion coefficient for B.")
@click.option("--alpha", default=-0.005, type=float, help="Alpha parameter.")
@click.option("--beta", default=10.0, type=float, help="Beta parameter.")
@click.option("--steps", default=150, type=int, help="Number of steps.")
@click.option("--output", default="image", help="Output file name.")
@click.option("--gif", default=False, help="Create gif")
def main(da, db, alpha, beta, steps, output, gif):
    print("generating pattern ... ")

    x, y = np.mgrid[0:WIDTH, 0:WIDTH]
    beta = 0.1 + 5 * (1 + np.sin(2 * np.pi * y / 50)) * (1 + np.sin(2 * np.pi * x / 50))

    def Ra(a, b):
        return a - a**3 - b + alpha

    def Rb(a, b):
        return (a - b) * beta

    eq = TwoDimensionalRDEquations(
        da, db, Ra, Rb, width=WIDTH, height=HEIGHT, dx=DX, dt=DT, steps=steps
    )

    if gif:
        eq.plot_time_evolution(f"{output}.gif", n_steps=steps)

    eq.plot_evolution_outcome(f"{output}.png", n_steps=steps)


if __name__ == "__main__":
    main()
