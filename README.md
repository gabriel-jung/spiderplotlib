# Spiderplotlib

**Simple spider/radar plots for Python with matplotlib.**

![Example Spider Plot](https://raw.githubusercontent.com/gabriel-jung/spiderplotlib/main/example.png)

## Installation (using PyPI)

```bash
pip install spiderplotlib
```

## Development (using uv)

```bash
git clone https://github.com/gabriel-jung/spiderplotlib
cd spiderplotlib
uv sync
```

## Quick Start

```python
import matplotlib.pyplot as plt
from spiderplotlib import spider_plot

# Algorithm performance
groups = [
    [0.89, 0.92, 0.78, 0.95, 0.88],
    [0.85, 0.88, 0.90, 0.82, 0.91],
]

labels = ['Precision', 'Recall', 'Speed', 'Memory', 'F1']

fig = spider_plot(
    groups=groups,
    labels=labels,
    title='Algorithm Comparison',
    group_names=['RF', 'XGBoost']
    
)

plt.show()
```

## API Reference

### `spider_plot()`

```python
spider_plot(
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
) -> mpl.figure.Figure
```

**Parameters:**

- `groups`: List of groups to compare (each contains values for all axes)
- `labels`: List of strings representing axis/parameter labels.
- `group_names`: Optional list of labels for each group (displayed in legend).
- `group_colors`: Optional list of colors for each group.
- `title`: Optional plot title string.
- `show_legend`: Whether to display legend (default: True).
- `show_values`: Whether to display maximum values on each axis (default: False).
- `show_scale`: Whether to display percentage scale indicators (default: True).
- `figsize`: Figure size as (width, height) tuple (default: (8, 8)).
- `alpha`: Transparency for filled areas, range 0-1 (default: 0.3).
- `grid_levels`: Custom grid levels as fractions (default: [0.2, 0.4, 0.6, 0.8, 1.0]).
- `value_format`: Format string for displayed values (default: "{:.2f}").
- `label_distance`: Distance of labels from center (default: 1.2).

**Returns:**

- `matplotlib.figure.Figure`: The created figure object.

## Advanced Usage

### Custom Colors

```python
fig = spider_plot(
    groups=groups,
    labels=labels,
    group_colors=['#1f77b4', '#ff7f0e'],
    alpha=0.4
)
```

### Adjust label distance

```python
fig = spider_plot(
    groups=groups,
    labels=long_labels,
    label_distance=1.4  # Move labels further out
)
```

## Examples

See `example.py` for complete working examples and `example.ipynb` for comprehensive exploration of features.
