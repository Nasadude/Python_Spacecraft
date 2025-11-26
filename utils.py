import json
import numpy as np
from matplotlib import pyplot as plt

# ---------------------------------------------
# Load JSON Configuration
# ---------------------------------------------
def load_config(path):
    with open(path, "r") as f:
        return json.load(f)


# ---------------------------------------------
# Planet color resolution (merge global + per-planet)
# ---------------------------------------------
def get_planet_colors(cfg, planet_name):
    global_colors = cfg.get("colors", {})
    planet_colors = cfg["planets"].get(planet_name, {}).get("colors", {})
    return {**global_colors, **planet_colors}


# ---------------------------------------------
# Extract and convert initial conditions (r0, v0)
# ---------------------------------------------
def get_initial_conditions(cfg, planet_name):
    planet_cfg = cfg["planets"][planet_name]

    r0_million_km = planet_cfg["position_at_perihelion"]  # in million km
    v0_kms = planet_cfg["velocity_at_perihelion"]          # in km/s

    r0 = np.array([r0_million_km * 1e9, 0.0], dtype=float)   # → meters
    v0 = np.array([0.0, -v0_kms * 1e3], dtype=float)         # → m/s

    return r0, v0

# ----------------------------------------------------------
# Time settings
# ----------------------------------------------------------
def get_time_settings(cfg, planet_cfg):
    """
    Uses planet-specific orbital_period_days if present.
    Otherwise falls back to Earth default (365 days).
    """

    time_step = cfg["numerical_method_settings"]["time_step"] \
        if "numerical_method_settings" in cfg else 3600

    sim_days = planet_cfg.get(
        "orbital_period_days",
        cfg.get("default_simulation_days", 365)  # fallback
    )

    t_max = sim_days * 24 * 3600
    t = np.arange(0, t_max, time_step)

    return time_step, t

# ---------------------------------------------
# Create the gravitational acceleration function
# ---------------------------------------------
def create_acceleration_fn(G, M):
    def acc_fn(r_vec):
        norm = np.linalg.norm(r_vec)
        return -(G * M / norm**3) * r_vec
    return acc_fn


# ---------------------------------------------
# Pre-allocate and set initial arrays
# ---------------------------------------------
def initialize_arrays(r0, v0, t):
    r = np.zeros((len(t), 2))
    v = np.zeros((len(t), 2))

    r[0] = r0
    v[0] = v0

    return r, v


# -----------------------------------------------------------
# Compute aphelion helper
# -----------------------------------------------------------
def compute_aphelion(r, v):
    """
    Identify aphelion and ensure it is not the first point.
    """
    distances = np.linalg.norm(r, axis=1)

    # Raw aphelion detection
    idx_ap = int(np.argmax(distances))

    # If index 0 → not a real aphelion → we need fallback
    if idx_ap == 0:
        # ignore first 5% of simulation and recompute
        cutoff = max(1, int(len(r) * 0.05))
        idx_ap = int(np.argmax(distances[cutoff:]) + cutoff)

    pos_ap = distances[idx_ap]
    vel_ap = v[idx_ap]

    return pos_ap, vel_ap, idx_ap


# -----------------------------------------------------------
# Numerical Integration Methods (Euler + RK4)
# -----------------------------------------------------------

def euler_step(r_old, v_old, dt, acc_fn):
    """Single Euler update step."""
    a_old = acc_fn(r_old)
    r_new = r_old + v_old * dt
    v_new = v_old + a_old * dt
    return r_new, v_new


def rk4_step(r_old, v_old, dt, acc_fn):
    """Single RK4 update step."""

    k1_v = acc_fn(r_old)
    k1_r = v_old

    k2_r = v_old + k1_v * (dt / 2)
    k2_v = acc_fn(r_old + k1_r * (dt / 2))

    k3_r = v_old + k2_v * (dt / 2)
    k3_v = acc_fn(r_old + k2_r * (dt / 2))

    k4_r = v_old + k3_v * dt
    k4_v = acc_fn(r_old + k3_r * dt)

    r_new = r_old + (dt / 6) * (k1_r + 2*k2_r + 2*k3_r + k4_r)
    v_new = v_old + (dt / 6) * (k1_v + 2*k2_v + 2*k3_v + k4_v)

    return r_new, v_new


def run_integration(method, r, v, dt, acc_fn):
    """
    Run either Euler or RK4 integration across all timesteps.
    Mutates r[] and v[] in place.
    """

    method = method.lower()

    for i in range(1, len(r)):

        if method == "euler":
            r[i], v[i] = euler_step(r[i-1], v[i-1], dt, acc_fn)

        elif method == "rk4":
            r[i], v[i] = rk4_step(r[i-1], v[i-1], dt, acc_fn)

        else:
            raise ValueError(f"Unknown numerical method '{method}'. Use 'euler' or 'rk4'.")


# -----------------------------------------------------------
# Plotting (existing function stays the same)
# -----------------------------------------------------------
def plot_orbit_3d(
    r, v, method_name, planet_name,
    pos_aphelion, vel_aphelion, idx_aphelion, colors
):
    
    print("Aphelion index:", idx_aphelion)
    print("r[0] (perihelion):", r[0])
    print("r[idx_aphelion] (aphelion):", r[idx_aphelion])
    print("Max distance (m):", pos_aphelion)
    print("Distance at perihelion:", np.linalg.norm(r[0]))
    plt.style.use(colors.get("background", "dark_background"))
    fig = plt.figure(figsize=(7, 12))
    ax = fig.add_subplot(111, projection="3d")

    # ----------------------------
    # Titles
    # ----------------------------
    plt.suptitle(
        f"{method_name.upper()} Method – {planet_name} Orbit",
        color="r", fontsize=18, weight="bold"
    )

    plt.title(
        f"Aphelion distance: {round(pos_aphelion/1e9,1)} million km\n"
        f"Aphelion speed: {round(vel_aphelion/1e3,1)} km/s",
        fontsize=14, color="orange"
    )

    # ----------------------------
    # Orbit path
    # ----------------------------
    ax.plot(
        r[:, 0], r[:, 1], 0,
        lw=2,
        color=colors.get("orbit", "white"),
        label=f"{planet_name} Orbit"
    )

    # ----------------------------
    # Sun
    # ----------------------------
    ax.scatter(
        0, 0, 0,
        s=1000,
        color=colors.get("sun", "yellow"),
        label="Sun"
    )

    # ----------------------------
    # PERIHELION (offset outward)
    # ----------------------------
    px, py = r[0]
    radius = np.linalg.norm([px, py])   # distance from Sun

    # small outward offset (0.2%)
    peri_offset = 0.002 * radius
    direction = np.array([px, py]) / radius

    perihelion_point = np.array([px, py]) + direction * peri_offset

    ax.scatter(
        perihelion_point[0],
        perihelion_point[1],
        0,
        s=200,
        color=colors.get("perihelion", "cyan"),
        label=f"{planet_name} Perihelion"
    )


    # ---------------------------------------
    # Aphelion
    # ---------------------------------------
    ax.scatter(
        r[idx_aphelion, 0],
        r[idx_aphelion, 1],
        0,
        s=200,
        color=colors.get("aphelion", "magenta"),
        label=f"{planet_name} Aphelion"
    )

    # ----------------------------
    # Legend
    # ----------------------------
    plt.axis("off")
    legend = plt.legend(loc="lower right", frameon=False)

    # Resize markers
    if len(legend.legend_handles) >= 4:
        legend.legend_handles[1]._sizes = [150]
        legend.legend_handles[2]._sizes = [80]
        legend.legend_handles[3]._sizes = [80]

    plt.show()
