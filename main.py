import numpy as np
from utils import (
    load_config,
    get_planet_colors,
    get_initial_conditions,
    get_time_settings,
    create_acceleration_fn,
    initialize_arrays,
    compute_aphelion,
    run_integration,
    plot_orbit_3d
)

# ---------------------------------------------
# Load and resolve config
# ---------------------------------------------
cfg = load_config("config.json")
planet_name = cfg["planet"]
method = cfg["numerical_method"]

colors = get_planet_colors(cfg, planet_name)
r0, v0 = get_initial_conditions(cfg, planet_name)
# Resolve planet config block
planet_cfg = cfg["planets"][planet_name]
dt, t = get_time_settings(cfg, planet_cfg)


# ---------------------------------------------
# Create simulation arrays
# ---------------------------------------------
r, v = initialize_arrays(r0, v0, t)

# ---------------------------------------------
# Physics
# ---------------------------------------------
G = 6.6743e-11
M_sun = 1.989e30
acc_fn = create_acceleration_fn(G, M_sun)

# ---------------------------------------------
# Run numerical integration
# ---------------------------------------------
run_integration(method, r, v, dt, acc_fn)

# ---------------------------------------------
# Compute aphelion
# ---------------------------------------------
pos_ap, vel_vec_ap, idx_ap = compute_aphelion(r, v)
vel_ap = np.linalg.norm(vel_vec_ap)

# ---------------------------------------------
# Visualize
# ---------------------------------------------
plot_orbit_3d(
    r=r,
    v=v,
    method_name=method,
    planet_name=planet_name,
    pos_aphelion=pos_ap,
    vel_aphelion=vel_ap,
    idx_aphelion=idx_ap,
    colors=colors
)
