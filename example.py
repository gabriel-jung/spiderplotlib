#!/usr/bin/env python3
"""Spiderplotlib example."""

from spiderplotlib import spider_plot
import matplotlib.pyplot as plt

# Algorithm performance comparison
groups = [
    [0.89, 0.92, 0.78, 0.95, 0.88],  # Random Forest
    [0.85, 0.88, 0.90, 0.82, 0.91],  # XGBoost
]

labels = ['Precision', 'Recall', 'Speed', 'Memory', 'F1']

fig = spider_plot(
    groups=groups,
    labels=labels,
    title='Algorithm Comparison',
    group_names=['Random Forest', 'XGBoost'],
    group_colors=['#1f77b4', '#ff7f0e'],
    show_legend=True,
    show_values=True,
    value_format="{:.2f}",    
    label_distance=1.3,
    figsize=(10, 10),
    show_scale=True,
    grid_levels=[0.2, 0.4, 0.6, 0.8, 1.0],
)

plt.show()
