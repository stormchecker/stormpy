"""Helpers for plotting Pareto curves of two-dimensional multi-objective queries.

Requires the ``plot`` extra: ``pip install stormpy[plot]``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from matplotlib.axes import Axes
import stormpy

__all__ = ["plot_convex_pareto_curve_demo", "prepare_multiobjective_result_for_plotting"]


def plot_convex_pareto_curve_demo(
    ax: Axes, underapprox_points: np.ndarray, overapprox_points: np.ndarray, lowerleft: Sequence[float], upperright: Sequence[float]
) -> None:
    """

    :param ax: The matplotlib axis to plot onto.
    :param underapprox_points: The points for the underapproximation
    :param overapprox_points: The points for the overapproximation of the Pareto-plot
    :param lowerleft: The lower left corner for the plot
    :param upperright: The upper right corner for the plot
    :return: Nothing
    """
    from scipy.spatial import ConvexHull

    ax.set_xlim(lowerleft[0], upperright[0])
    ax.set_ylim(lowerleft[1], upperright[1])
    ax.grid()
    under_hull = ConvexHull(underapprox_points)
    over_hull = ConvexHull(overapprox_points)
    ax.set_facecolor("r")
    ax.fill(overapprox_points[over_hull.vertices, 0], overapprox_points[over_hull.vertices, 1], "w", 1)
    ax.fill(underapprox_points[under_hull.vertices, 0], underapprox_points[under_hull.vertices, 1], "g", 1)


def _prepare_points_for_convex_pareto_plotting(
    points: Sequence[Sequence[float]],
    lower_corner: Sequence[float],
    upper_corner: Sequence[float],
    multi_obj_formula: stormpy.logic.MultiObjectiveFormula,
) -> np.ndarray:
    """

    :param points:
    :param lower_corner:
    :param upper_corner:
    :param multi_obj_formula:
    :return:
    """

    def direction_as_operation(dir: stormpy.logic.OptimizationDirection) -> Callable[[Sequence[float]], float]:
        return max if dir == stormpy.logic.OptimizationDirection.MAXIMIZE else min

    if multi_obj_formula.nr_subformulas != 2:
        raise RuntimeError("Plotting is only supported for two dimensions")
    directions = [f.optimality_type for f in multi_obj_formula.subformulas]

    origin_x = min(lower_corner[0], upper_corner[0]) if directions[0] == stormpy.logic.OptimizationDirection.MAXIMIZE else max(lower_corner[0], upper_corner[0])
    origin_y = min(lower_corner[1], upper_corner[1]) if directions[1] == stormpy.logic.OptimizationDirection.MAXIMIZE else max(lower_corner[1], upper_corner[1])
    origin = np.array([[origin_x, origin_y]])
    x_cut_x = direction_as_operation(directions[0])([p[0] for p in points])
    x_cut = np.array([[x_cut_x, origin_y]])
    y_cut_y = direction_as_operation(directions[1])([p[1] for p in points])
    y_cut = np.array([[origin_x, y_cut_y]])

    points = np.concatenate((np.array(points), origin, x_cut, y_cut), axis=0)
    return points


def prepare_multiobjective_result_for_plotting(
    result: stormpy.results.ExplicitParetoCurveCheckResult,
    lower_corner: Sequence[float],
    upper_corner: Sequence[float],
    formula: stormpy.logic.MultiObjectiveFormula,
) -> list[np.ndarray]:
    """
    Takes a multiobjective model checking results and prepares it for plotting.

    :param result: The multiobjective model checking result for a two-dimensional query.
    :param lower_corner: The lower left corner used for plotting
    :param upper_corner: The upper right corner used for plotting
    :param formula: The multiobjective formula
    :return: A list with two arrays of points representing an under- and overapproximation of the vertices
    """
    results = [result.get_under_approximation(), result.get_over_approximation()]
    return [_prepare_points_for_convex_pareto_plotting(h.vertices, lower_corner, upper_corner, formula) for h in results]
