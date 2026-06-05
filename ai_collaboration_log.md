# AI Collaboration Log: 3D Crutch Movement Visualiser

This document outlines the collaborative process between the user and the AI assistant (Antigravity) in developing a web-based 3D visualiser for crutch motion data.

## Project Objective
The goal was to create a web-based 3D visualiser that animates the movement of a crutch using raw sensor data (`Accel first walk.csv` and `rotation first walk.csv`). The visualiser needed to accurately represent the crutch's orientation and translation in space, and provide an interactive UI for playback control.

## Phase 1: Planning and Foundation
1. **Requirements Gathering**:
   - Use Three.js for 3D rendering.
   - Represent the crutch with simple cylinder shapes and an inertial measurement unit (IMU) as a red cuboid mounted 1 meter from the ground.
   - Coordinate system: Y is up, X is forward, Z is right (relative to the crutch's vertical orientation).
   - Implement playback controls: play/pause, reverse, step frame, and a scrubbable timeline.
   - Synchronize acceleration (in g) and angular velocity (in rad/s) data to drive the animation.

2. **Initial Implementation**:
   - The AI generated a single-file solution (`index.html`) using HTML, CSS, and JavaScript.
   - Designed a modern, dark-themed "glassmorphism" UI with real-time data panels for Gyroscope and Accelerometer readings.
   - Implemented data parsing and pre-integration:
     - **Rotation**: Integrated angular velocity (gyroscope data) into quaternions for smooth 3D orientation.
     - **Position**: Double-integrated accelerometer data to calculate translational movement.

## Phase 2: Iteration and Debugging
Once the initial build was running locally via a Python HTTP server, several issues were identified and resolved collaboratively:

1. **Visibility Adjustments**:
   - *Issue*: The initial crutch model was too thin and the camera was positioned too far away.
   - *Fix*: The AI increased the shaft diameter (to 2.5cm), enlarged the tip and cuff, and moved the default camera position closer for better visibility.

2. **Position Integration & Drift Mitigation**:
   - *Issue*: The crutch immediately flew off-screen vertically. The user correctly hypothesized that the accelerometer data had already been sanitized (gravity removed), causing the AI's gravity compensation algorithm to apply a phantom -1g acceleration.
   - *Fix*: The AI removed the gravity subtraction step. To counter the inherent drift in double-integrating accelerometer data without a magnetometer, the AI implemented a stronger velocity damping factor (0.95), resulting in realistic translational motion that remained within the scene.

3. **Enhancement: "Set Origin" Feature**:
   - *Request*: The user wanted the ability to reset the origin to the crutch's current position and rotation at any point during playback.
   - *Implementation*: The AI added a "Set Origin" button (`⊕`) and an `O` keyboard shortcut. The code was updated to store offset quaternions and position vectors, dynamically re-centering the scene around the crutch's current pose.

## Phase 3: Deployment Preparation
1. **GitHub Pages Readiness**:
   - *Request*: The user wanted to host the visualiser on GitHub Pages.
   - *Implementation*: The AI moved `index.html` from the `visualiser/` subdirectory to the repository root and updated the data fetch paths from relative `../` to local `./`. This structure allows GitHub Pages to serve the site directly from the repository root without configuration changes.

## Conclusion
Through iterative development, user feedback, and AI-assisted coding, the project successfully evolved from raw CSV data into a fully functional, interactive 3D motion visualiser. The final application accurately maps the sensor data to the 3D model, provides robust playback controls, and is structured for seamless web hosting.
