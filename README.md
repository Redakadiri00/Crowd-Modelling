# Crowd Modelling Using Social Force Model

## Description
This project simulates crowd dynamics using the **Social Force Model**. It models the movement of pedestrians in a confined space with the goal of reaching the nearest exit while avoiding collisions with other pedestrians and obstacles. The simulation incorporates physics-based interactions and provides a visual representation of pedestrian movement.

## Features
- Simulation of pedestrian dynamics using the Social Force Model.
- Real-time animation of pedestrian movement.
- Avoidance of collisions between pedestrians and with obstacles.
- Support for multiple exits, with pedestrians dynamically selecting the nearest one.
- Customizable parameters for the number of pedestrians, room size, and pedestrian attributes (e.g., mass, radius, desired speed).

## Key Components
1. **Pedestrian Dynamics**:
   - Each pedestrian is represented with unique attributes such as mass, radius, and desired speed.
   - Calculation of forces:
     - Driving force towards the target (exit).
     - Repulsive forces between pedestrians to avoid collisions.
     - Repulsive forces between pedestrians and walls/obstacles.

2. **Environment**:
   - Configurable room dimensions.
   - Placement of obstacles within the room.
   - Single or multiple exits for pedestrian egress.

3. **Visualization**:
   - Animated simulation using `matplotlib`.
   - Color-coded pedestrians for easy identification.
   - Obstacles and exits clearly marked.

## Technologies Used
- **Programming Language**: Python
- **Libraries**: 
  - `numpy` for numerical computations.
  - `matplotlib` for visualization and animation.
  - `random` for generating random pedestrian attributes.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/crowd-modelling.git
