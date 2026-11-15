import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def rot_x(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0,   c,  -s],
        [0.0,   s,   c],
    ])


def rot_y(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [  c, 0.0,   s],
        [0.0, 1.0, 0.0],
        [ -s, 0.0,   c],
    ])


def case_b_rotation_matrix(t: float, omega: float = 1.0, alpha: float = np.pi / 4) -> np.ndarray:
    """
    Case B rotation matrix for the unprimed frame:
        R(t) = R_y(-alpha) @ R_x(omega * t) @ R_y((omega / 4) * t + alpha)
    """
    return rot_y(-alpha) @ rot_x(omega * t) @ rot_y(0.25 * omega * t + alpha)


def case_b_trace_explicit(t: np.ndarray, R: float = 1.0, omega: float = 1.0, alpha: float = np.pi / 4) -> np.ndarray:
    """
    Closed-form trajectory of the unprimed +z pole P(t) = R * z_hat(t) for Case B:
        X(t) = (sqrt(2)/2) R [ sin(omega*t/4 + pi/4) - cos(omega*t/4 + pi/4) cos(omega*t) ]
        Y(t) = -R sin(omega*t) cos(omega*t/4 + pi/4)
        Z(t) = (sqrt(2)/2) R [ sin(omega*t/4 + pi/4) + cos(omega*t/4 + pi/4) cos(omega*t) ]
    """
    u = 0.25 * omega * t + alpha
    X = R * (np.cos(alpha) * np.sin(u) - np.sin(alpha) * np.cos(u) * np.cos(omega * t))
    Y = -R * np.sin(omega * t) * np.cos(u)
    Z = R * (np.sin(alpha) * np.sin(u) + np.cos(alpha) * np.cos(u) * np.cos(omega * t))
    return np.vstack([X, Y, Z])


def generate_overview_figure(R: float = 1.0, omega: float = 1.0, alpha: float = np.pi / 4, out_path: str = "case_b_overview.png"):
    T = 8.0 * np.pi / omega
    t_dense = np.linspace(0.0, T, 2000)
    P = case_b_trace_explicit(t_dense, R=R, omega=omega, alpha=alpha)

    fig = plt.figure(figsize=(14, 10), dpi=140)
    fig.suptitle("Case B: Spherical Trace of Unprimed +z Pole $P(t) = R\\,\\hat{z}(t)$\n"
                 "$R(t) = R_y(-\\alpha)\\,R_x(\\omega t)\\,R_y(\\frac{\\omega}{4}t + \\alpha),\\ \\alpha = 45^\\circ$",
                 fontsize=13, fontweight="bold")

    # 1. 3D Sphere + Full Trace
    ax3d = fig.add_subplot(2, 2, 1, projection="3d")
    u_sph = np.linspace(0, 2 * np.pi, 48)
    v_sph = np.linspace(0, np.pi, 24)
    xs = R * np.outer(np.cos(u_sph), np.sin(v_sph))
    ys = R * np.outer(np.sin(u_sph), np.sin(v_sph))
    zs = R * np.outer(np.ones_like(u_sph), np.cos(v_sph))
    ax3d.plot_surface(xs, ys, zs, color="lightsteelblue", alpha=0.15, edgecolor="none")
    ax3d.plot_wireframe(xs, ys, zs, color="slategray", alpha=0.15, linewidth=0.4, rstride=2, cstride=4)

    ax3d.plot(P[0], P[1], P[2], color="#d9480f", linewidth=2.0, label="Full Trace $P(t)$")
    ax3d.scatter([P[0, 0]], [P[1, 0]], [P[2, 0]], color="limegreen", s=50, zorder=5, label="$P(0) = (0,0,R)$")

    ax3d.set_xlim([-1.2 * R, 1.2 * R])
    ax3d.set_ylim([-1.2 * R, 1.2 * R])
    ax3d.set_zlim([-1.2 * R, 1.2 * R])
    ax3d.set_box_aspect((1, 1, 1))
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Z")
    ax3d.set_title("3D Trace on Sphere of Radius R")
    ax3d.legend(loc="upper left", fontsize=8)
    ax3d.view_init(elev=24, azim=38)

    # 2. XY Projection
    ax_xy = fig.add_subplot(2, 2, 2)
    theta_c = np.linspace(0, 2 * np.pi, 300)
    ax_xy.plot(R * np.cos(theta_c), R * np.sin(theta_c), "--", color="gray", alpha=0.5, label="Equator $r=R$")
    ax_xy.plot(P[0], P[1], color="#1c7ed6", linewidth=1.6)
    ax_xy.scatter([P[0, 0]], [P[1, 0]], color="limegreen", s=40, zorder=5, label="$t=0$")
    ax_xy.set_aspect("equal")
    ax_xy.set_xlabel("X")
    ax_xy.set_ylabel("Y")
    ax_xy.set_title("Top View (XY Projection)")
    ax_xy.grid(True, alpha=0.3)
    ax_xy.legend(fontsize=8)

    # 3. XZ Projection
    ax_xz = fig.add_subplot(2, 2, 3)
    ax_xz.plot(R * np.cos(theta_c), R * np.sin(theta_c), "--", color="gray", alpha=0.5)
    ax_xz.plot(P[0], P[2], color="#2b8a3e", linewidth=1.6)
    ax_xz.scatter([P[0, 0]], [P[2, 0]], color="limegreen", s=40, zorder=5, label="$t=0$")
    ax_xz.set_aspect("equal")
    ax_xz.set_xlabel("X")
    ax_xz.set_ylabel("Z")
    ax_xz.set_title("Side View (XZ Projection — Precession Axis Plane)")
    ax_xz.grid(True, alpha=0.3)
    ax_xz.legend(fontsize=8)

    # 4. Coordinates vs Time
    ax_t = fig.add_subplot(2, 2, 4)
    norm_t = t_dense / T
    ax_t.plot(norm_t, P[0] / R, label="$X(t)/R$", color="#e03131")
    ax_t.plot(norm_t, P[1] / R, label="$Y(t)/R$", color="#1971c2")
    ax_t.plot(norm_t, P[2] / R, label="$Z(t)/R$", color="#2f9e44")
    ax_t.set_xlabel("Normalized Time $t / T$  ($T = 8\\pi / \\omega$)")
    ax_t.set_ylabel("Coordinate / R")
    ax_t.set_title("Coordinates of $P(t)$ Over One Full Period")
    ax_t.grid(True, alpha=0.3)
    ax_t.legend(fontsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(out_path)
    plt.close(fig)


def create_animation(
    R: float = 1.0,
    omega: float = 1.0,
    alpha: float = np.pi / 4,
    n_frames: int = 180,
    fps: int = 25,
    gif_path: str = "case_b_trace.gif",
    show_interactive: bool = False,
):
    T = 8.0 * np.pi / omega
    t_frames = np.linspace(0.0, T, n_frames, endpoint=False)
    t_dense = np.linspace(0.0, T, 1600)
    P_full = case_b_trace_explicit(t_dense, R=R, omega=omega, alpha=alpha)

    phi = np.linspace(0.0, 2.0 * np.pi, 200)

    fig = plt.figure(figsize=(10, 8), dpi=110)
    ax = fig.add_subplot(111, projection="3d")

    # Translucent reference sphere
    u_sph = np.linspace(0, 2 * np.pi, 40)
    v_sph = np.linspace(0, np.pi, 20)
    xs = R * np.outer(np.cos(u_sph), np.sin(v_sph))
    ys = R * np.outer(np.sin(u_sph), np.sin(v_sph))
    zs = R * np.outer(np.ones_like(u_sph), np.cos(v_sph))
    ax.plot_surface(xs, ys, zs, color="lightsteelblue", alpha=0.12, edgecolor="none")
    ax.plot_wireframe(xs, ys, zs, color="slategray", alpha=0.14, linewidth=0.4, rstride=2, cstride=4)

    # Inertial axes (faint reference)
    axis_len = 1.15 * R
    ax.plot([-axis_len, axis_len], [0, 0], [0, 0], color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.plot([0, 0], [-axis_len, axis_len], [0, 0], color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.plot([0, 0], [0, 0], [-axis_len, axis_len], color="gray", linestyle=":", linewidth=0.8, alpha=0.5)

    # Faint full trajectory guide
    ax.plot(P_full[0], P_full[1], P_full[2], color="#ffa94d", alpha=0.28, linewidth=1.0, linestyle="--", label="Full Period Path")

    # Dynamic plot elements
    unprimed_circle_line, = ax.plot([], [], [], color="#1c7ed6", linewidth=2.2, label="Unprimed Circle ($yz$ plane)")
    primed_circle_line, = ax.plot([], [], [], color="#2b8a3e", linewidth=2.0, linestyle="-.", label="Primed Circle ($y'z'$ plane)")
    z0_circle_line, = ax.plot([], [], [], color="#862e9c", linewidth=1.1, linestyle=":", alpha=0.7, label="$z=0$ Dynamic Plane ($xy$)")

    intersect_line, = ax.plot([], [], [], color="#f59f00", linewidth=2.4, label="Intersection Axis $\\pm R\\hat{y}(t)$")
    intersect_pts, = ax.plot([], [], [], "o", color="#f59f00", markersize=6)

    normal_unprimed_line, = ax.plot([], [], [], color="#1c7ed6", linewidth=1.6, alpha=0.85, label="Unprimed Normal $\\hat{x}(t)$")
    normal_primed_line, = ax.plot([], [], [], color="#2b8a3e", linewidth=1.6, alpha=0.85, label="Primed Normal $\\hat{x}'(t)$")

    trace_line, = ax.plot([], [], [], color="#d9480f", linewidth=2.6, label="Trace of $+z$ Pole $P(t)$")
    pole_pt, = ax.plot([], [], [], "o", color="#e03131", markersize=8, label="Unprimed $+z$ Pole $P(t)$")
    pole_vec, = ax.plot([], [], [], color="#e03131", linewidth=1.8)

    title_text = ax.set_title("", fontsize=11, fontweight="bold", pad=12)

    ax.set_xlim([-1.2 * R, 1.2 * R])
    ax.set_ylim([-1.2 * R, 1.2 * R])
    ax.set_zlim([-1.2 * R, 1.2 * R])
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=24, azim=38)
    ax.legend(loc="upper left", bbox_to_anchor=(-0.12, 1.02), fontsize=8.5, framealpha=0.9)

    def update(frame_idx: int):
        t = t_frames[frame_idx]
        R_mat = case_b_rotation_matrix(t, omega=omega, alpha=alpha)

        # Unprimed orthonormal basis vectors
        x_hat = R_mat[:, 0]
        y_hat = R_mat[:, 1]
        z_hat = R_mat[:, 2]

        # Primed orthonormal basis vectors (45-deg coupled about shared intersection line y_hat)
        R_prime = R_mat @ rot_y(-alpha)
        xp_hat = R_prime[:, 0]
        yp_hat = R_prime[:, 1]  # Identical to y_hat
        zp_hat = R_prime[:, 2]

        # 1. Unprimed circle in span(y_hat, z_hat)
        c_unprimed = R * (np.outer(y_hat, np.cos(phi)) + np.outer(z_hat, np.sin(phi)))
        unprimed_circle_line.set_data(c_unprimed[0], c_unprimed[1])
        unprimed_circle_line.set_3d_properties(c_unprimed[2])

        # 2. Primed circle in span(yp_hat, zp_hat)
        c_primed = R * (np.outer(yp_hat, np.cos(phi)) + np.outer(zp_hat, np.sin(phi)))
        primed_circle_line.set_data(c_primed[0], c_primed[1])
        primed_circle_line.set_3d_properties(c_primed[2])

        # 3. z=0 dynamic plane great circle in span(x_hat, y_hat)
        c_z0 = R * (np.outer(x_hat, np.cos(phi)) + np.outer(y_hat, np.sin(phi)))
        z0_circle_line.set_data(c_z0[0], c_z0[1])
        z0_circle_line.set_3d_properties(c_z0[2])

        # 4. Line of intersection across +-R * y_hat
        inter_seg = np.column_stack([-R * y_hat, R * y_hat])
        intersect_line.set_data(inter_seg[0], inter_seg[1])
        intersect_line.set_3d_properties(inter_seg[2])
        intersect_pts.set_data(inter_seg[0], inter_seg[1])
        intersect_pts.set_3d_properties(inter_seg[2])

        # 5. Normals x_hat and xp_hat
        n_u = np.column_stack([np.zeros(3), 0.85 * R * x_hat])
        normal_unprimed_line.set_data(n_u[0], n_u[1])
        normal_unprimed_line.set_3d_properties(n_u[2])

        n_p = np.column_stack([np.zeros(3), 0.85 * R * xp_hat])
        normal_primed_line.set_data(n_p[0], n_p[1])
        normal_primed_line.set_3d_properties(n_p[2])

        # 6. Pole P(t) = R * z_hat and trace up to current time t
        P_now = R * z_hat
        pole_pt.set_data([P_now[0]], [P_now[1]])
        pole_pt.set_3d_properties([P_now[2]])

        p_seg = np.column_stack([np.zeros(3), P_now])
        pole_vec.set_data(p_seg[0], p_seg[1])
        pole_vec.set_3d_properties(p_seg[2])

        t_hist = np.linspace(0.0, max(t, 1e-6), max(2, frame_idx * 8))
        P_hist = case_b_trace_explicit(t_hist, R=R, omega=omega, alpha=alpha)
        trace_line.set_data(P_hist[0], P_hist[1])
        trace_line.set_3d_properties(P_hist[2])

        angle_deg = np.degrees(np.arccos(np.clip(np.dot(x_hat, xp_hat), -1.0, 1.0)))
        title_text.set_text(
            f"Case B Spherical Trace of Unprimed +z Pole  |  t/T = {t/T:.2f}  |  "
            f"Inter-plane Angle = {angle_deg:.1f}°"
        )
        return (
            unprimed_circle_line,
            primed_circle_line,
            z0_circle_line,
            intersect_line,
            intersect_pts,
            normal_unprimed_line,
            normal_primed_line,
            trace_line,
            pole_pt,
            pole_vec,
            title_text,
        )

    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000 // fps, blit=False)

    if gif_path:
        writer = PillowWriter(fps=fps)
        anim.save(gif_path, writer=writer)

    if show_interactive:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Animate Case B Gyroscopic Spherical Trace")
    parser.add_argument("--R", type=float, default=1.0, help="Sphere/circle radius R")
    parser.add_argument("--omega", type=float, default=1.0, help="Unprimed angular rate omega")
    parser.add_argument("--frames", type=int, default=160, help="Number of animation frames")
    parser.add_argument("--fps", type=int, default=25, help="Frames per second")
    parser.add_argument("--gif", type=str, default="case_b_trace.gif", help="Output GIF filename")
    parser.add_argument("--overview", type=str, default="case_b_overview.png", help="Output overview PNG filename")
    parser.add_argument("--show", action="store_true", help="Open interactive 3D Matplotlib window")
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    # Verify numerical consistency between matrix product R(t)e_z and explicit equations
    t_test = np.linspace(0, 8 * np.pi / args.omega, 50)
    for ti in t_test:
        p_mat = args.R * (case_b_rotation_matrix(ti, omega=args.omega) @ np.array([0.0, 0.0, 1.0]))
        p_exp = case_b_trace_explicit(ti, R=args.R, omega=args.omega).ravel()
        assert np.allclose(p_mat, p_exp, atol=1e-12), f"Mismatch at t={ti}: {p_mat} vs {p_exp}"

    generate_overview_figure(R=args.R, omega=args.omega, out_path=args.overview)
    create_animation(
        R=args.R,
        omega=args.omega,
        n_frames=args.frames,
        fps=args.fps,
        gif_path=args.gif,
        show_interactive=args.show,
    )
    print(f"Saved overview plot to: {args.overview}")
    print(f"Saved 3D animation to:  {args.gif}")
