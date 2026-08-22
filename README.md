# Autonomous Quadruped Navigation & Perception Stack

A ROS 2-based autonomous navigation and perception stack for the **Unitree Go2 quadruped**, developed and evaluated in **Gazebo Harmonic**.

The project integrates quadruped locomotion, multi-sensor perception, state estimation, SLAM, localization, path planning, obstacle avoidance, and autonomous navigation into a unified robotics system.

> **Project Status:** 🚧 In Development

---

## Overview

The goal of this project is to develop a complete autonomous robotics pipeline for a quadruped robot:

```text
                    Unitree Go2
                         │
                  Gazebo Harmonic
                         │
                      ROS 2
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      LiDAR             RGB-D            IMU
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                    Perception
                         ↓
                 State Estimation
                       EKF
                         ↓
                      SLAM
                         ↓
                   Localization
                         ↓
                  Path Planning
                         ↓
                Obstacle Avoidance
                         ↓
                      cmd_vel
                         ↓
                   CHAMP / Gait
                         ↓
                     Unitree Go2
```

The project is being developed incrementally, with each subsystem tested independently before integration.

---

## Objectives

The main objectives are to:

* Build and simulate a **Unitree Go2 quadruped** in Gazebo Harmonic.
* Integrate ROS 2 with the quadruped's locomotion stack.
* Integrate and process **LiDAR, RGB-D camera, IMU, and joint-state data**.
* Develop a sensor-based perception pipeline for obstacle detection.
* Implement **EKF-based sensor fusion** for robot state estimation.
* Integrate **LiDAR-based SLAM** and localization.
* Develop global path planning and reactive obstacle avoidance.
* Connect high-level navigation commands with the quadruped locomotion system.
* Evaluate autonomous navigation performance in simulated environments.

---

## Technology Stack

| Category         | Technology        |
| ---------------- | ----------------- |
| Robot            | Unitree Go2       |
| Middleware       | ROS 2 Jazzy       |
| Simulator        | Gazebo Harmonic   |
| Programming      | Python, C++       |
| Locomotion       | CHAMP             |
| Robot Control    | `ros2_control`    |
| Visualization    | RViz2             |
| Sensors          | LiDAR, RGB-D, IMU |
| State Estimation | EKF               |
| Mapping          | SLAM              |
| Planning         | A*, Nav2          |
| Version Control  | Git / GitHub      |
| OS               | Ubuntu 24.04 LTS  |

---

## System Architecture

### 1. Quadruped Simulation

The Unitree Go2 is simulated in Gazebo Harmonic with ROS 2 providing communication between the simulation, controllers, sensors, and navigation stack.

```text
Gazebo Harmonic
      │
      ├── Go2 Model
      ├── Sensors
      ├── Joint Simulation
      └── Physics
             │
             ↓
           ROS 2
```

---

### 2. Locomotion

The low-level locomotion layer is based on the CHAMP quadruped controller.

```text
Desired Velocity
      ↓
Locomotion Controller
      ↓
Gait Generator
      ↓
Foot Trajectory
      ↓
Inverse Kinematics
      ↓
Joint Commands
      ↓
Unitree Go2
```

The initial goal is to establish stable walking, turning, and stopping before integrating autonomous navigation.

---

### 3. Perception

The robot will use multiple sensors to perceive its environment.

```text
             ┌── LiDAR
             │
             ├── RGB Camera
Sensors ─────┼── Depth Camera
             │
             └── IMU
                    │
                    ↓
              Sensor Processing
                    │
                    ↓
                 Perception
```

The perception layer will initially focus on obstacle detection and environmental representation.

---

### 4. State Estimation

IMU and odometry measurements will be combined using an Extended Kalman Filter.

```text
          IMU
           │
           │
           ├──────→ EKF ─────→ Estimated Robot State
           │
        Odometry
```

The estimated state will provide a more robust pose and velocity estimate for downstream localization and navigation.

---

### 5. Mapping & Localization

LiDAR data will be used to construct an environment representation and estimate the robot's position.

```text
LiDAR
  │
  ↓
SLAM
  │
  ├── Map
  │
  └── Robot Pose
          │
          ↓
     Localization
```

---

### 6. Path Planning

The navigation system will contain both global and local planning components.

```text
             Goal
              │
              ↓
       Global Planner
            A*
              │
              ↓
         Global Path
              │
              ↓
      Local Obstacle Avoidance
              │
              ↓
          cmd_vel
```

A custom A* implementation will initially be used to understand and validate the planning pipeline. Nav2 integration will then provide a more complete navigation framework.

---

### 7. Autonomous Behavior

The final system should demonstrate autonomous behavior such as:

```text
User provides goal
        ↓
Robot plans path
        ↓
Robot starts walking
        ↓
Obstacle detected
        ↓
Local avoidance / replanning
        ↓
Robot continues toward goal
        ↓
Goal reached
```

---

# Development Roadmap

The project is being developed in several phases.

### Phase 0 — Go2 Simulation & Locomotion

* [ ] Set up Unitree Go2 simulation
* [ ] Verify Gazebo Harmonic integration
* [ ] Verify ROS 2 communication
* [ ] Understand CHAMP architecture
* [ ] Verify `ros2_control`
* [ ] Verify joint states
* [ ] Verify odometry
* [ ] Implement/test forward walking
* [ ] Implement/test rotation
* [ ] Implement/test stopping
* [ ] Document TF tree and ROS graph

### Phase 1 — Sensor Integration

* [ ] LiDAR
* [ ] IMU
* [ ] RGB camera
* [ ] Depth camera
* [ ] Joint states
* [ ] Sensor TF frames
* [ ] RViz2 visualization
* [ ] Verify sensor topics and message rates

### Phase 2 — Perception

* [ ] LiDAR preprocessing
* [ ] Obstacle detection
* [ ] Depth-based obstacle detection
* [ ] Sensor coordinate transformations
* [ ] Basic obstacle representation

### Phase 3 — State Estimation

* [ ] Understand robot motion model
* [ ] Configure odometry
* [ ] Integrate IMU
* [ ] Implement/configure EKF
* [ ] Validate filtered pose
* [ ] Compare raw and filtered estimates

### Phase 4 — Mapping & Localization

* [ ] Integrate LiDAR-based SLAM
* [ ] Generate occupancy maps
* [ ] Validate mapping accuracy
* [ ] Implement localization
* [ ] Validate robot pose in known maps

### Phase 5 — Path Planning

* [ ] Implement occupancy-grid representation
* [ ] Implement A*
* [ ] Generate collision-free paths
* [ ] Add path smoothing
* [ ] Evaluate planning performance
* [ ] Compare custom planner with Nav2

### Phase 6 — Obstacle Avoidance

* [ ] Local obstacle detection
* [ ] Reactive velocity control
* [ ] Dynamic replanning
* [ ] Recovery behavior
* [ ] Safe stopping

### Phase 7 — Navigation + Locomotion Integration

* [ ] Connect planner to `cmd_vel`
* [ ] Connect navigation to CHAMP
* [ ] Convert velocity commands to locomotion behavior
* [ ] Autonomous waypoint navigation
* [ ] Obstacle avoidance while walking
* [ ] Goal detection

### Phase 8 — Evaluation

* [ ] Navigation success rate
* [ ] Goal-position error
* [ ] Collision rate
* [ ] Path length
* [ ] Planning time
* [ ] Localization error
* [ ] Navigation experiments
* [ ] Final demonstration video

---

# Repository Structure

The repository will evolve as new subsystems are implemented.

```text
autonomous-quadruped-navigation/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── src/
│   ├── quadruped_perception/
│   ├── quadruped_state_estimation/
│   ├── quadruped_mapping/
│   ├── quadruped_planning/
│   └── quadruped_navigation/
│
├── config/
│
├── launch/
│
├── rviz/
│
├── maps/
│
├── worlds/
│
└── docs/
```

The exact package structure will be finalized as the implementation progresses.

---

# Current Status

### 🟡 Phase 0 — Simulation Setup

Current focus:

* Unitree Go2 simulation
* Gazebo Harmonic
* ROS 2 Jazzy
* CHAMP locomotion
* `ros2_control`

The navigation and perception components are **planned but not yet implemented**.

---

# Planned Demonstration

The final demonstration will show the Unitree Go2 autonomously navigating a simulated environment.

### Scenario

```text
             ┌─────────────────────────────┐
             │                             │
             │   Start                     │
             │     🤖                     │
             │      │                      │
             │      │                      │
             │      └─────────────┐        │
             │                    │        │
             │              ███████│       │
             │              █      │       │
             │              █      └────┐  │
             │              █           │  │
             │                          🎯│
             │                             │
             └─────────────────────────────┘
```

The robot will:

1. Receive a navigation goal.
2. Localize itself within the environment.
3. Plan a collision-free path.
4. Walk using the quadruped locomotion system.
5. Detect obstacles using onboard sensors.
6. Avoid or replan around obstacles.
7. Continue toward the goal.
8. Stop when the goal is reached.

---

# Evaluation

Once the complete system is operational, performance will be evaluated using measurable metrics rather than only visual demonstrations.

Potential metrics include:

* **Navigation success rate**
* **Collision rate**
* **Final goal-position error**
* **Path length**
* **Planning time**
* **Localization error**
* **Obstacle avoidance success rate**
* **Computation frequency**

Experimental results will be added to this README as the project develops.

---

# Learning Goals

This project is intended to provide practical experience with:

* ROS 2 architecture
* ROS 2 topics, services and actions
* TF2
* Gazebo simulation
* `ros2_control`
* Quadruped locomotion
* Inverse kinematics
* Gait generation
* Sensor integration
* LiDAR processing
* RGB-D perception
* IMU processing
* Sensor fusion
* Extended Kalman Filters
* SLAM
* Localization
* Occupancy grids
* A* path planning
* Nav2
* Obstacle avoidance
* Autonomous robot behaviors
* Robotics system integration

---

# Project Philosophy

The project is developed incrementally.

Each subsystem should be:

1. **Implemented**
2. **Tested independently**
3. **Visualized**
4. **Integrated**
5. **Evaluated**

The objective is not simply to assemble existing ROS 2 packages, but to understand how the individual components interact to form a complete autonomous robotics system.

---

# License

This project contains original work developed for educational and portfolio purposes.

Third-party components, including the Unitree Go2 simulation and CHAMP-based locomotion stack, remain subject to their respective licenses and attribution requirements.

See the individual third-party repositories for their licensing information.
