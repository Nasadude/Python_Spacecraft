---

# 🌍 **Orbital Mechanics Simulator**

### Numerical Integration of Planetary Orbits (Euler & RK4)

This project simulates the **orbit of any planet** around the Sun using:

* **Euler Method**
* **Runge–Kutta 4th Order Method (RK4)**

All simulation parameters—including the selected planet, integration method, time settings, and colors—are controlled through a single **config.json** file.

The simulator computes:

* The full orbital trajectory
* The **aphelion** (farthest point from the Sun)
* The orbital **speed at aphelion**
* A customizable **3D visualization**

---

# 📁 **Project Structure**

```
project/
│
├── main.py              # Entry point: loads config, runs integration, plots
├── utils.py             # Numerical methods, gravity, plotting, helpers
├── config.json          # User-editable settings (planets, colors, times)
└── README.md            # Documentation
```

---

# ⚙️ **Configuration (config.json)**

All simulation settings are controlled through `config.json`.

### ✔ Example Layout (updated format)

```json
{
  "planet": "Earth",
  "method": "rk4",

  "global_colors": {
    "sun": "yellow",
    "orbit": "white",
    "perihelion": "cyan",
    "aphelion": "magenta",
    "background": "dark_background"
  },

  "time_settings": {
    "time_step_hours": 1,
    "simulation_days": 365
  },

  "planets": {
    "Mercury": {
      "position_at_perihelion": 46.0,
      "velocity_at_perihelion": 58.98,
      "colors": {
        "orbit": "orange",
        "perihelion": "red",
        "aphelion": "purple"
      }
    },

    "Venus": {
      "position_at_perihelion": 107.5,
      "velocity_at_perihelion": 35.02,
      "colors": {
        "orbit": "gold",
        "perihelion": "white",
        "aphelion": "darkred"
      }
    },

    "Earth": {
      "position_at_perihelion": 147.1,
      "velocity_at_perihelion": 30.29,
      "colors": {
        "orbit": "tab:blue",
        "perihelion": "grey",
        "aphelion": "blue"
      }
    },

    "Mars": {
      "position_at_perihelion": 206.7,
      "velocity_at_perihelion": 26.50,
      "colors": {
        "orbit": "red",
        "perihelion": "yellow",
        "aphelion": "brown"
      }
    },

    "Jupiter": {
      "position_at_perihelion": 740.5,
      "velocity_at_perihelion": 13.1,
      "colors": {
        "orbit": "peru",
        "perihelion": "goldenrod",
        "aphelion": "saddlebrown"
      }
    },

    "Saturn": {
      "position_at_perihelion": 1357.6,
      "velocity_at_perihelion": 9.7,
      "colors": {
        "orbit": "khaki",
        "perihelion": "gold",
        "aphelion": "darkkhaki"
      }
    },

    "Uranus": {
      "position_at_perihelion": 2732.7,
      "velocity_at_perihelion": 6.8,
      "colors": {
        "orbit": "cyan",
        "perihelion": "lightcyan",
        "aphelion": "turquoise"
      }
    },

    "Neptune": {
      "position_at_perihelion": 4471.1,
      "velocity_at_perihelion": 5.4,
      "colors": {
        "orbit": "royalblue",
        "perihelion": "lightskyblue",
        "aphelion": "darkblue"
      }
    },

    "Pluto": {
      "position_at_perihelion": 4436.8,
      "velocity_at_perihelion": 4.7,
      "colors": {
        "orbit": "tan",
        "perihelion": "bisque",
        "aphelion": "sienna"
      }
    }
  }
}
```

---

# 🧠 **How to Use**

### 1. Choose a Planet

Set the `"planet"` field:

```json
"planet": "Mars"
```

### 2. Choose numerical method

```json
"method": "euler"
# or
"method": "rk4"
```

### 3. Adjust time settings

```json
"time_settings": {
  "time_step_hours": 1,
  "simulation_days": 365
}
```

### 4. Customize colors globally

```json
"global_colors": {
  "sun": "yellow",
  "orbit": "white",
  "perihelion": "cyan",
  "aphelion": "magenta",
  "background": "dark_background"
}
```

### 5. Override colors per planet (optional)

Each planet can override the defaults.

---

# 🪐 **Units Used**

To simplify the config:

* **Distances**: millions of km (10⁶ km)

  * Earth perihelion = **147.1**
* **Velocities**: km/s

  * Earth perihelion velocity = **30.29**

Internally the simulator:

* Converts distances → meters
* Converts velocities → meters/second

---

# 🔢 **Numerical Methods**

### ✔ Euler Method

Simple but lower accuracy.

### ✔ RK4 Method

High precision, stable, ideal for orbital mechanics.

---

# 📈 **Output**

The simulator generates a **3D visualization** that includes:

* Planet's orbital path
* Sun position
* **Perihelion** marker
* **Aphelion** marker
* Title showing:

  * Distance at aphelion
  * Speed at aphelion
  * Numerical method used

Colors dynamically match your `config.json`.

---

# 🚀 **Running the Simulation**

From terminal:

```
python3 main.py
```

---
