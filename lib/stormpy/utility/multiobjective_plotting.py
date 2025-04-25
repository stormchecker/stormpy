import numpy as np
import stormpy


def plot_convex_pareto_curve_demo(ax, underapprox_points, overapprox_points, lowerleft, upperright):
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


def _prepare_points_for_convex_pareto_plotting(points, lower_corner, upper_corner, multi_obj_formula):
    """

    :param points:
    :param lower_corner:
    :param upper_corner:
    :param multi_obj_formula:
    :return:
    """

    def direction_as_operation(dir: stormpy.OptimizationDirection):
        return max if dir == stormpy.OptimizationDirection.Maximize else min

    if multi_obj_formula.nr_subformulas != 2:
        raise RuntimeError("Plotting is only supported for two dimensions")
    directions = [f.optimality_type for f in multi_obj_formula.subformulas]

    origin_x = min(lower_corner[0], upper_corner[0]) if directions[0] == stormpy.OptimizationDirection.Maximize else max(lower_corner[0], upper_corner[0])
    origin_y = min(lower_corner[1], upper_corner[1]) if directions[1] == stormpy.OptimizationDirection.Maximize else max(lower_corner[1], upper_corner[1])
    origin = np.array([[origin_x, origin_y]])
    x_cut_x = direction_as_operation(directions[0])([p[0] for p in points])
    x_cut = np.array([[x_cut_x, origin_y]])
    y_cut_y = direction_as_operation(directions[1])([p[1] for p in points])
    y_cut = np.array([[origin_x, y_cut_y]])

    points = np.concatenate((np.array(points), origin, x_cut, y_cut), axis=0)
    return points


def prepare_multiobjective_result_for_plotting(result, lower_corner, upper_corner, formula):
    """
    Takes a multiobjective model checking results and prepares it for plotting.

    :param result: The multiobjective model checkign result for a two-dimensional model checkign result.
    :param lower_corner: The lower left corner used for plotting
    :param upper_corner: The upper right corner used for plotting
    :param formula: The multiobjective formula
    :return: A tuple with two sets of points representing an under- and overapproximation of the vertices
    """
    results = [result.get_underapproximation(), result.get_overapproximation()]
    return [_prepare_points_for_convex_pareto_plotting(h.vertices, lower_corner, upper_corner, formula) for h in results]
