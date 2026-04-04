import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle
import matplotlib.transforms as transforms

def run_gci_simulation():
    # 1. Generate 2500 points from a 2D Standard Normal distribution
    np.random.seed(42)
    n_points = 2500
    points = np.random.normal(0, 1, (n_points, 2))

    # 2. Setup the plot 
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.05, bottom=0.35, right=0.55)
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_title("Gaussian Correlation Inequality", fontsize=14, weight='bold')

    # Scatter the Gaussian points
    ax.scatter(points[:, 0], points[:, 1], c='gray', alpha=0.3, s=10)

    # Initial parameters
    init_w_k = 1.0
    init_w_l = 1.0
    init_rot_l = 45.0

    # 3. Draw Strip K (Vertical, Blue)
    # Expanded length to 20 to act as an "infinite" strip
    patch_k = Rectangle((-init_w_k/2, -10), init_w_k, 20, color='blue', alpha=0.2)
    ax.add_patch(patch_k)

    # 4. Draw Strip L (Horizontal, Red)
    # Expanded length to 20 to act as an "infinite" strip
    patch_l = Rectangle((-10, -init_w_l/2), 20, init_w_l, color='red', alpha=0.2)
    t_start = ax.transData
    t_rot = transforms.Affine2D().rotate_deg_around(0, 0, init_rot_l)
    patch_l.set_transform(t_rot + t_start)
    ax.add_patch(patch_l)

    # Text box placed on the Figure window
    props = dict(boxstyle='round,pad=1', facecolor='#f8f9fa', alpha=1.0, edgecolor='gray')
    text_results = fig.text(0.60, 0.60, "", fontsize=13, bbox=props, family='monospace', verticalalignment='center')

    # 5. The Update Function
    def update(val):
        wk = s_wk.val
        wl = s_wl.val
        rot = s_rot.val

        # Update visual patches
        patch_k.set_width(wk)
        patch_k.set_xy((-wk/2, -10))
        
        patch_l.set_height(wl)
        patch_l.set_xy((-10, -wl/2))
        t_rot_new = transforms.Affine2D().rotate_deg_around(0, 0, rot)
        patch_l.set_transform(t_rot_new + t_start)

        # Calculate logical intersections computationally
        in_k = np.abs(points[:, 0]) <= wk/2
        
        theta = np.radians(-rot)
        c, s = np.cos(theta), np.sin(theta)
        rot_y = points[:, 0] * s + points[:, 1] * c
        in_l = np.abs(rot_y) <= wl/2

        in_both = in_k & in_l

        # Calculate empirical probabilities
        p_k = np.sum(in_k) / n_points
        p_l = np.sum(in_l) / n_points
        p_both = np.sum(in_both) / n_points
        product = p_k * p_l

        # Update text output
        status = "✓ THEOREM HOLDS" if p_both >= product else "X ERROR"
        res_str = (f"Empirical Simulation Data\n"
                   f"Total Points: {n_points}\n"
                   f"--------------------------\n"
                   f"Points in K:    {np.sum(in_k)}\n"
                   f"Points in L:    {np.sum(in_l)}\n"
                   f"Points in Both: {np.sum(in_both)}\n\n"
                   f"Probability Calculations\n"
                   f"--------------------------\n"
                   f"P(K)        = {p_k:.4f}\n"
                   f"P(L)        = {p_l:.4f}\n"
                   f"P(K) * P(L) = {product:.4f}\n"
                   f"P(K ∩ L)    = {p_both:.4f}\n\n"
                   f"--------------------------\n"
                   f"{status}")
        text_results.set_text(res_str)
        fig.canvas.draw_idle()

    # 6. Define Sliders
    axcolor = 'lightgray'
    ax_wk = plt.axes([0.05, 0.20, 0.50, 0.03], facecolor=axcolor)
    ax_wl = plt.axes([0.05, 0.13, 0.50, 0.03], facecolor=axcolor)
    ax_rot = plt.axes([0.05, 0.06, 0.50, 0.03], facecolor=axcolor)

    s_wk = Slider(ax_wk, 'Width K', 0.2, 4.0, valinit=init_w_k)
    s_wl = Slider(ax_wl, 'Width L', 0.2, 4.0, valinit=init_w_l)
    s_rot = Slider(ax_rot, 'Rotation L', 0.0, 90.0, valinit=init_rot_l)

    # Bind sliders to update function
    s_wk.on_changed(update)
    s_wl.on_changed(update)
    s_rot.on_changed(update)

    # Initialize text and show
    update(None)
    plt.show()

if __name__ == "__main__":
    run_gci_simulation()