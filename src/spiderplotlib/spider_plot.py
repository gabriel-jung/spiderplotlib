"""Spider plot functionality."""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import List, Optional, Union


def _calculate_text_position(label: str, angle: float, distance: float = 1.2) -> tuple:
    """Calculate text position at specified distance."""
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    return x, y


def _get_adaptive_circle_radius(value_text: str) -> float:
    """Calculate circle radius for value display."""
    return max(0.04, 0.03 + 0.015 * len(value_text))


def spider_plot(
    groups: List[Union[List[float], np.ndarray]],
    labels: List[str],
    group_names: Optional[List[str]] = None,
    group_colors: Optional[List[str]] = None,
    title: Optional[str] = None,
    show_legend: bool = True,
    show_values: bool = False,
    show_scale: bool = True,
    figsize: tuple = (8, 8),
    alpha: float = 0.3,
    grid_levels: Optional[List[float]] = None,
    value_format: str = "{:.2f}",
    label_distance: float = 1.2,
) -> mpl.figure.Figure:
    """Create a spider plot (radar chart).

    Args:
        groups: List of groups to compare (each contains values for all axes)
        labels: List of axis labels
        group_names: Labels for each group (displayed in legends)
        group_colors: Colors for each group
        title: Plot title
        show_legend: Show legend (True/False)
        show_values: Show max values on axes (True/False)
        show_scale: Show percentage scale (True/False)
        figsize: Figure size (width, height)
        alpha: Transparency (0-1)
        grid_levels: Custom grid levels
        value_format: Value display format
        label_distance: Distance of labels from center (default: 1.2)

    Returns:
        matplotlib.figure.Figure
        
    Examples:
        >>> groups = [[0.8, 0.6, 0.9], [0.7, 0.8, 0.5]]
        >>> labels = ['Speed', 'Power', 'Accuracy']
        >>> fig = spider_plot(groups, labels)
    """
    # Input validation
    if len(groups) == 0:
        raise ValueError("Groups cannot be empty")

    if len(labels) == 0:
        raise ValueError("Labels cannot be empty")

    # Convert groups to list format
    groups = [_convert_to_list(group) for group in groups]

    # Validate groups consistency
    expected_length = len(labels)
    for i, group in enumerate(groups):
        if len(group) != expected_length:
            raise ValueError(
                f"Group {i} has length {len(group)}, expected {expected_length}"
            )

        # Check for non-numeric values
        for j, value in enumerate(group):
            if not isinstance(value, (int, float, np.number)):
                raise ValueError(f"Group {i}, value {j} is not numeric: {value}")

    # Set defaults
    if group_names is None:
        group_names = [f"Group {i + 1}" for i in range(len(groups))]

    if group_colors is None:
        base_colors = plt.cm.tab10.colors
        colors = [base_colors[i % len(base_colors)] for i in range(len(groups))]
    else:
        colors = group_colors

    if grid_levels is None:
        grid_levels = [0.2, 0.4, 0.6, 0.8, 1.0]

    # Validate group_names and colors
    if len(group_names) != len(groups):
        raise ValueError(
            f"group_names length {len(group_names)} doesn't match groups length {len(groups)}"
        )

    if len(colors) != len(groups):
        raise ValueError(
            f"Colors length {len(colors)} doesn't match groups length {len(groups)}"
        )

    # Per-parameter normalization
    original_groups = [group[:] for group in groups]

    # Find max value for each parameter across all entries
    num_parameters = len(labels)
    param_max_values = []

    for param_idx in range(num_parameters):
        param_values = [group[param_idx] for group in groups]
        param_max = max(param_values)
        param_max_values.append(param_max if param_max > 0 else 1.0)

    # Normalize each group independently per parameter
    normalized_groups = []
    for group in groups:
        normalized_group = []
        for param_idx, value in enumerate(group):
            param_max = param_max_values[param_idx]
            normalized_value = value / param_max
            normalized_group.append(normalized_value)
        normalized_groups.append(normalized_group)

    # Normalize data
    groups = normalized_groups

    # Create figure
    fig, ax = plt.subplots(figsize=figsize, subplot_kw={"polar": False})

    # Plot setup
    N = len(labels)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # Add title
    if title is not None:
        ax.set_title(title, fontsize=16, pad=20)

    # Draw grid circles with percentage scale
    for level in grid_levels:
        xs = level * np.cos(theta)
        ys = level * np.sin(theta)
        grid = mpl.patches.Polygon(
            np.column_stack([xs, ys]), fill=False, color="lightgray", linewidth=1
        )
        ax.add_patch(grid)

        # Add scale indicators as percentages if requested
        if show_scale:
            percentage_level = level * 100
            ax.text(
                (level * np.cos(theta)[0] + level * np.cos(theta)[-1]) / 2,
                (level * np.sin(theta)[0] + level * np.sin(theta)[-1]) / 2,
                f"{int(percentage_level)}%",
                rotation=(90 - 180 / N),
                fontsize=10,
                color="0.05",
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.1",
                    ec="0.6",
                    fc="white",
                    alpha=0.8,
                ),
            )

    # Plot each group
    for i, group in enumerate(groups):
        xs = np.array(group) * np.cos(theta)
        ys = np.array(group) * np.sin(theta)

        # Create polygon for the group
        poly = mpl.patches.Polygon(
            np.column_stack([xs, ys]),
            fc=mpl.colors.to_rgba(colors[i], alpha),
            ec=mpl.colors.to_rgba(colors[i], 1.0),
            lw=2,
        )

        ax.add_patch(poly)
        ax.scatter(xs, ys, color=colors[i], s=50, edgecolor="black", linewidth=1)

    # Add axis lines and labels
    for i, t in enumerate(theta):
        # Add axis line
        line = mpl.lines.Line2D(
            [0, np.cos(t)], [0, np.sin(t)], color="lightgray", linewidth=1
        )
        ax.add_line(line)

        # Show max values in adaptive circles if requested
        if show_values and i < N:
            values = [group[i] for group in original_groups]
            max_value = max(values)
            value_text = value_format.format(max_value)

            # Position at the top of the axis
            value_x = 1.0 * np.cos(t)
            value_y = 1.0 * np.sin(t)

            # Draw circle with adaptive size
            circle_radius = _get_adaptive_circle_radius(value_text)
            circle = mpl.patches.Circle(
                (value_x, value_y),
                radius=circle_radius,
                facecolor="white",
                edgecolor="black",
                linewidth=0.8,
                alpha=0.9,
            )
            ax.add_patch(circle)

            # Add value text with slight adjustment
            ax.text(
                value_x,
                value_y - 0.008,
                value_text,
                fontsize=9,
                weight="bold",
                color="black",
                ha="center",
                va="center",
            )

        # Add axis label with manual distance control
        if i < N:
            angle = i * 2 * np.pi / N
            x, y = _calculate_text_position(labels[i], angle, label_distance)

            # Adjust angle for text rotation
            text_angle = np.rad2deg(angle)
            if x < 0:
                text_angle = text_angle - 180

            ax.text(
                x,
                y,
                labels[i],
                rotation=text_angle,
                ha="center",
                va="center",
                fontsize=12,
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    ec="white",
                    fc="white",
                    alpha=0.7,
                ),
            )

    # Add legend
    if show_legend:
        legend_elements = []
        for i, legend in enumerate(group_names):
            legend_elements.append(
                mpl.patches.Patch(
                    facecolor=mpl.colors.to_rgba(colors[i], alpha),
                    edgecolor=mpl.colors.to_rgba(colors[i], 1.0),
                    label=legend,
                )
            )

        ax.legend(
            handles=legend_elements,
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            borderaxespad=0,
            frameon=False,
            fontsize=11,
        )

    # Final formatting
    ax.set_aspect("equal")
    limit = max(1.3, label_distance + 0.1)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    plt.axis("off")

    plt.tight_layout()
    return fig


def _convert_to_list(data) -> list:
    """Convert input data to a list if it isn't already."""
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif not isinstance(data, list):
        return list(data)
    return data
