#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tools" / ".matplotlib-cache"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon, Rectangle


DEFAULT_OUTPUT_DIR = ROOT / "ref" / "programmatic-diagrams" / "batch-001"
DPI = 160
FIGSIZE = (12.8, 7.2)


BLUE = "#2563eb"
GREEN = "#22a06b"
RED = "#e5484d"
DARK = "#202124"
GRAY = "#8b929c"
GRID = "#d5d9df"
PALE_BLUE = "#dbeafe"
PALE_GREEN = "#dcfce7"
PALE_RED = "#fee2e2"
PALE_ORANGE = "#ffedd5"


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans Mono",
            "mathtext.fontset": "dejavusans",
            "axes.edgecolor": DARK,
            "axes.linewidth": 0.9,
            "axes.labelsize": 15,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


def clean_axes(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.grid(True, color=GRID, linestyle="-", linewidth=0.6, alpha=0.75)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def bias_variance(path: Path) -> None:
    x = np.linspace(0.05, 1, 400)
    bias = 0.95 * np.exp(-4 * x) + 0.04
    variance = 0.05 + 0.92 * x**2.7
    total = bias + variance + 0.12
    i = int(np.argmin(total))
    fig, ax = plt.subplots(figsize=FIGSIZE)
    clean_axes(ax, "Model Complexity", "Prediction Error")
    ax.plot(x, bias, color=BLUE, lw=3, label=r"Bias$^2$")
    ax.plot(x, variance, color=RED, lw=3, label="Variance")
    ax.plot(x, total, color=DARK, lw=3, label="Total Error")
    ax.axvline(x[i], color=GRAY, ls="--", lw=2)
    ax.scatter([x[i]], [total[i]], s=90, color="green", zorder=5)
    ax.text(x[i], total[i] + 0.22, "Optimal complexity", color="green", ha="center", fontsize=16)
    ax.text(0.12, 1.1, "Underfitting", fontsize=16)
    ax.text(0.78, 1.1, "Overfitting", fontsize=16)
    ax.legend(frameon=False, loc="center right", fontsize=16)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.25)
    save(fig, path)


def kmeans(path: Path) -> None:
    rng = np.random.default_rng(7)
    c1 = rng.normal([-1.8, -1.4], [0.45, 0.42], (28, 2))
    c2 = rng.normal([-1.3, 1.8], [0.45, 0.38], (28, 2))
    c3 = rng.normal([1.8, 0.3], [0.45, 0.45], (30, 2))
    centers = np.array([c1.mean(0), c2.mean(0), c3.mean(0)])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    clean_axes(ax, "Feature 1", "Feature 2")
    xx, yy = np.meshgrid(np.linspace(-3.2, 3.2, 500), np.linspace(-3, 3, 500))
    grid = np.c_[xx.ravel(), yy.ravel()]
    dist = ((grid[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    z = np.argmin(dist, axis=1).reshape(xx.shape)
    ax.contourf(xx, yy, z, levels=[-0.5, 0.5, 1.5, 2.5], colors=[PALE_BLUE, PALE_GREEN, PALE_RED], alpha=0.72)
    ax.contour(xx, yy, z, levels=[0.5, 1.5], colors=[GRAY], linewidths=1.2)
    ax.scatter(c1[:, 0], c1[:, 1], s=55, color=BLUE, edgecolor="#174ea6", label="Cluster 1")
    ax.scatter(c2[:, 0], c2[:, 1], s=55, color="#3aa655", marker="s", edgecolor="#1b7f36", label="Cluster 2")
    ax.scatter(c3[:, 0], c3[:, 1], s=70, color=RED, marker="^", edgecolor="#b42328", label="Cluster 3")
    for n, (cx, cy) in enumerate(centers, 1):
        ax.scatter([cx], [cy], s=180, marker="+", color="black", linewidths=3, label="Centroid" if n == 1 else None)
        ax.text(cx + 0.12, cy + 0.12, rf"$m_{n}$", fontsize=18)
    ax.legend(frameon=True, loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=15)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3, 3)
    save(fig, path)


def linear_regression(path: Path) -> None:
    x = np.array([650, 800, 980, 1200, 1300, 1500, 1650, 1800, 2050, 2200, 2400, 2580, 2730, 3000])
    y_line = 0.25 * x + 20
    y = y_line + np.array([-35, -12, -10, -18, 45, -35, 55, -30, 35, -35, 20, 30, 45, 80])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.94, bottom=0.14, top=0.92)
    clean_axes(ax, "House Size", "Price")
    ax.scatter(x, y, s=60, color=BLUE)
    ax.plot([600, 3050], [0.25 * 600 + 20, 0.25 * 3050 + 20], color=RED, lw=2.5)
    for xi, yi, yl in zip(x[3:11:2], y[3:11:2], y_line[3:11:2]):
        ax.plot([xi, xi], [yl, yi], color=GRAY, lw=1.4)
    ax.annotate("Observed data", xy=(1650, y[6]), xytext=(1320, 620), arrowprops=dict(arrowstyle="->", lw=0.9), fontsize=11)
    ax.annotate("Best-fit line", xy=(2700, 0.25 * 2700 + 20), xytext=(2790, 650), arrowprops=dict(arrowstyle="->", lw=0.9), fontsize=11)
    ax.annotate("Residual error", xy=(1500, y[5]), xytext=(1640, 330), arrowprops=dict(arrowstyle="->", lw=0.9), fontsize=11)
    ax.text(2870, 790, r"$y = mx + b$", color=RED, fontsize=15)
    ax.set_xlim(500, 3150)
    ax.set_ylim(100, 900)
    save(fig, path)


def gradient_descent(path: Path) -> None:
    x = np.linspace(-3, 3, 400)
    y = 0.35 * (x - 0.5) ** 2 + 0.5
    pts_x = np.array([-2.6, -2.2, -1.8, -1.35, -0.95, -0.55, -0.2, 0.15])
    pts_y = 0.35 * (pts_x - 0.5) ** 2 + 0.5
    fig, ax = plt.subplots(figsize=FIGSIZE)
    clean_axes(ax, "Parameter $w$", "Cost $J(w)$")
    ax.plot(x, y, color=DARK, lw=3)
    ax.scatter(pts_x, pts_y, color=BLUE, s=75, zorder=5)
    for a, b in zip(range(len(pts_x) - 1), range(1, len(pts_x))):
        ax.annotate("", xy=(pts_x[b], pts_y[b]), xytext=(pts_x[a], pts_y[a]), arrowprops=dict(arrowstyle="->", color=DARK, lw=1.8))
    ax.scatter([0.5], [0.5], color="green", s=95, zorder=6)
    ax.text(0.5, 0.26, "Minimum cost", color="green", ha="center", fontsize=15)
    ax.annotate("Negative gradient direction", xy=(pts_x[1], pts_y[1]), xytext=(-1.35, 3.1), arrowprops=dict(arrowstyle="->"), fontsize=14)
    ax.annotate("Learning rate step", xy=(pts_x[3], pts_y[3]), xytext=(-1.3, 2.35), arrowprops=dict(arrowstyle="->"), fontsize=14)
    ax.annotate("Convergence", xy=(pts_x[-2], pts_y[-2]), xytext=(-1.7, 0.55), arrowprops=dict(arrowstyle="->"), fontsize=14)
    ax.set_xlim(-3, 3.2)
    ax.set_ylim(0, 4.0)
    save(fig, path)


def train_test_split(path: Path) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.axis("off")
    n = 25
    train = 20
    x0, y0, w, h = 0.06, 0.45, 0.88, 0.14
    cw = w / n
    for i in range(n):
        color = PALE_BLUE if i < train else PALE_ORANGE
        ax.add_patch(Rectangle((x0 + i * cw, y0), cw, h, facecolor=color, edgecolor="#4b5563", lw=1))
    ax.axvline(x0 + train * cw, ymin=0.43, ymax=0.62, color=DARK, ls="--", lw=1.5)
    ax.annotate("", xy=(x0, y0 + h + 0.12), xytext=(x0 + w, y0 + h + 0.12), arrowprops=dict(arrowstyle="]-[", lw=1.5, color=DARK))
    ax.text(x0 + w / 2, y0 + h + 0.17, "Full dataset", ha="center", fontsize=18)
    ax.annotate("", xy=(x0, y0 + h + 0.04), xytext=(x0 + train * cw, y0 + h + 0.04), arrowprops=dict(arrowstyle="]-[", lw=1.5, color=DARK))
    ax.text(x0 + train * cw / 2, y0 + h + 0.08, "Train 80%", ha="center", fontsize=16)
    ax.annotate("", xy=(x0 + train * cw, y0 + h + 0.04), xytext=(x0 + w, y0 + h + 0.04), arrowprops=dict(arrowstyle="]-[", lw=1.5, color=DARK))
    ax.text(x0 + train * cw + (w - train * cw) / 2, y0 + h + 0.08, "Test 20%", ha="center", fontsize=16)
    ax.text(x0 + train * cw / 2, y0 - 0.08, "Training set", ha="center", color="#174ea6", fontsize=18)
    ax.text(x0 + train * cw + (w - train * cw) / 2, y0 - 0.08, "Test set", ha="center", color="#c2410c", fontsize=18)
    ax.text(x0 + train * cw / 2, y0 - 0.18, "Model learns only from training data", ha="center", fontsize=14)
    ax.text(x0 + train * cw + (w - train * cw) / 2, y0 - 0.18, "Final evaluation on test data", ha="center", fontsize=14)
    save(fig, path)


def confusion_matrix(path: Path) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.axis("off")
    left, bottom, cw, ch = 0.36, 0.25, 0.20, 0.18
    row_w, head_h = 0.18, 0.11
    cells = [("True Positive", PALE_GREEN, 0, 1), ("False Negative", PALE_RED, 1, 1), ("False Positive", PALE_RED, 0, 0), ("True Negative", PALE_GREEN, 1, 0)]
    for text, color, col, row in cells:
        ax.add_patch(Rectangle((left + col * cw, bottom + row * ch), cw, ch, facecolor=color, edgecolor=GRAY, lw=1.2))
        ax.text(left + col * cw + cw / 2, bottom + row * ch + ch / 2, text, ha="center", va="center", fontsize=13, weight="bold", color="#166534" if color == PALE_GREEN else "#991b1b")
    headers = ["Predicted Positive", "Predicted Negative"]
    rows = ["Actual Positive", "Actual Negative"]
    for col, text in enumerate(headers):
        ax.add_patch(Rectangle((left + col * cw, bottom + 2 * ch), cw, head_h, facecolor="white", edgecolor=GRAY, lw=1.2))
        ax.text(left + col * cw + cw / 2, bottom + 2 * ch + head_h / 2, text, ha="center", va="center", fontsize=11.5, weight="bold")
    row_labels = ["Actual\nNegative", "Actual\nPositive"]
    for row, text in enumerate(row_labels):
        ax.add_patch(Rectangle((left - row_w, bottom + row * ch), row_w, ch, facecolor="white", edgecolor=GRAY, lw=1.2))
        ax.text(left - row_w / 2, bottom + row * ch + ch / 2, text, ha="center", va="center", fontsize=11.5, weight="bold", linespacing=1.05)
    ax.annotate(
        "Precision uses\npredicted positives",
        xy=(left + cw * 0.50, bottom + 2 * ch + head_h + 0.01),
        xytext=(left + cw * 0.50, bottom + 2 * ch + head_h + 0.13),
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", color="#166534", lw=1.0),
        fontsize=10,
        color="#166534",
    )
    ax.annotate(
        "Recall uses\nactual positives",
        xy=(left - row_w - 0.01, bottom + 1.5 * ch),
        xytext=(0.13, bottom + 1.5 * ch),
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", color="#174ea6", lw=1.0),
        fontsize=10,
        color="#174ea6",
    )
    save(fig, path)


def roc_curve(path: Path) -> None:
    x = np.linspace(0, 1, 400)
    y = 1 - np.exp(-7 * x)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    clean_axes(ax, "False Positive Rate", "True Positive Rate")
    ax.fill_between(x, y, 0, color=PALE_BLUE, alpha=0.85)
    ax.plot(x, y, color=BLUE, lw=3, label="ROC curve")
    ax.plot([0, 1], [0, 1], color=GRAY, lw=2, ls=(0, (5, 5)), label="Random classifier")
    ax.text(0.38, 0.45, "AUC", color=BLUE, fontsize=22)
    ax.annotate("Better classifier", xy=(0.12, 0.88), xytext=(0.04, 0.95), arrowprops=dict(arrowstyle="->", color=BLUE), color=BLUE, fontsize=15)
    ax.legend(loc="lower right", frameon=True, fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(fig, path)


def overfit_underfit(path: Path) -> None:
    rng = np.random.default_rng(4)
    x = np.linspace(0, 1, 16)
    y = 0.4 + 0.35 * np.sin(1.5 * np.pi * x) + rng.normal(0, 0.045, len(x))
    xs = np.linspace(0, 1, 300)
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE, sharex=True, sharey=True)
    titles = ["Underfitting", "Good Fit", "Overfitting"]
    for ax, title in zip(axes, titles):
        ax.scatter(x, y, color=BLUE, s=34)
        ax.set_title(title, fontsize=18)
        ax.grid(True, color=GRID, linestyle="--", linewidth=0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
    axes[0].plot(xs, 0.62 - 0.15 * xs, color=RED, lw=2.5)
    axes[1].plot(xs, 0.4 + 0.35 * np.sin(1.5 * np.pi * xs), color=RED, lw=2.5)
    coef = np.polyfit(x, y, 10)
    axes[2].plot(xs, np.polyval(coef, xs), color=RED, lw=2.5)
    save(fig, path)


def regularization(path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    theta = np.linspace(0, 2 * math.pi, 400)
    for ax, title in zip(axes, ["L1 Regularization\nSparse solution", "L2 Regularization\nSmall weights"]):
        ax.set_title(title, fontsize=20)
        ax.axhline(0, color=GRAY, lw=1)
        ax.axvline(0, color=GRAY, lw=1)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.2, 2.2)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xlabel(r"$w_1$", fontsize=18)
        ax.set_ylabel(r"$w_2$", fontsize=18, rotation=0, labelpad=12)
        for r in [0.8, 1.15, 1.5, 1.85]:
            ex = 1.25 * r * np.cos(theta) + 0.45
            ey = 0.7 * r * np.sin(theta) + 0.45
            rot = np.deg2rad(-28)
            xx = ex * np.cos(rot) - ey * np.sin(rot)
            yy = ex * np.sin(rot) + ey * np.cos(rot)
            ax.plot(xx, yy, color=GRAY, lw=1.1)
    diamond = np.array([[0, 1.25], [1.45, 0], [0, -1.25], [-1.45, 0]])
    axes[0].add_patch(Polygon(diamond, closed=True, facecolor="#60a5fa", edgecolor="#0f6fad", alpha=0.65, lw=2))
    axes[0].scatter([0.72], [0.62], color="#dc2626", s=70, zorder=5)
    axes[0].annotate("Regularized\nsolution", xy=(0.72, 0.62), xytext=(1.05, 1.05), arrowprops=dict(arrowstyle="->"), fontsize=14)
    axes[0].text(-1.85, -0.95, r"$||\mathbf{w}||_1 \leq C$", fontsize=18)
    axes[1].add_patch(Circle((0, 0), 1.15, facecolor="#60a5fa", edgecolor="#0f6fad", alpha=0.65, lw=2))
    axes[1].scatter([0.82], [0.8], color="#dc2626", s=70, zorder=5)
    axes[1].annotate("Regularized\nsolution", xy=(0.82, 0.8), xytext=(1.18, 1.12), arrowprops=dict(arrowstyle="->"), fontsize=14)
    axes[1].text(-0.45, -1.55, r"$||\mathbf{w}||_2^2 \leq C$", fontsize=18)
    save(fig, path)


RENDERERS = {
    "02-bias-variance": bias_variance,
    "03-kmeans": kmeans,
    "04-linear-regression": linear_regression,
    "05-gradient-descent": gradient_descent,
    "06-train-test-split": train_test_split,
    "07-confusion-matrix": confusion_matrix,
    "11-roc-curve": roc_curve,
    "12-overfit-underfit": overfit_underfit,
    "17-regularization": regularization,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render deterministic ML math/plot diagrams.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--only", choices=sorted(RENDERERS), nargs="*")
    return parser.parse_args()


def main() -> int:
    setup()
    args = parse_args()
    selected = args.only or list(RENDERERS)
    for slug in selected:
        path = args.output_dir / f"{slug}.png"
        print(path)
        RENDERERS[slug](path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
