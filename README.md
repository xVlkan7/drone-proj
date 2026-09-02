# drone-proj

blog:

8/14/26 - built a pacman-style game inside ROS2 for fun before I started working on PX4 and getting more into actual drone work. was a good skills check for ROS2 knowledge

8/10/26 - had to re build this project and downgrade to jazzy rather than lute because of some weird issue. spent enough time working on this today, will keep working later this week.

8/3/26 - learned all the basics of ROS2, such as nodes, topics, actions, services, and parameters. overall the system generally makes sense, but will need to do some testing to see how this can all tie together. being able to run a specific set of nodes without opening 4 terminals would be nice, that has gotten kinda annoying especially with docker. currently operating in a 2D space, so making a small project like bumper cars in that space would be a good test before I attempt 3D space.

7/30/26 - Got the project setup today, just checked out the tutorial. Seems pretty cool, I like the system so far. Having it run inside an ubuntu container is adding some difficulties but its good learning experience.


## Roadmap

#### COMPLETE - Phase 0 - Learning basics, tutorials, installs
	Need
	1. Git repo, docker, C++ (17/20), Python/Bash
	2. ROS2, either Jazzy or LTS
	3. Cmake
	4. colcon - used with ROS2 to build packages
	Deliverable:
	create the repo, make sure everything works on linux. this includes setting up an initial project, vscode extensions and linters, environments, etc.
	- [ ] repo setup
	- [ ] chatgpt working
	- [ ] docker setup
	- [ ] readme setup

#### COMPLETE - Phase 1 - Learning ROS2
	Still not on drones yet, just learning basics. Most of this is still in the tutorial in the docs
	1. Nodes
	2. Topics
	3. Publishers
	4. Subscribers
	5. Services
	6. Actions
	7. Parameters
	8. Launch Files
	
	Some mini projects:
	1. Hello ROS
	2. Talker
	3. Listener
	4. Camera node
	5. Controller node
	6. NOTE: right now you are working in 2D space, maybe making a small game where you avoid obstacles and get an orb could be a cool mini project? you could start with manual control then later have an automation tool/train AI to complete it.
	
	Example:
	1. Camera node
	2. Publishes an image
	3. Detector node
	4. Publishes target position
	5. Controller node
	6. Publishes desired velocity
	
	Deliverable for this phase:
	The mini ROS2 pacman game

#### Phase 2 - Learn PX4
	This is where drones come in, but without hardware yet
	
	Basics:
	1. Flight stack
	2. Sensors
	3. Flight modes
	4. PID loops
	5. Position controller
	6. Reading docs, etc.
	
	MAVLink is also useful. Main way for computers to talk to drones.
	
	Deliverable for this phase:
	Diagram how computer → MAVLink → PX4 → Motors


#### Phase 3 - Simulation
	Setup Gazebo and PX4 SITL (software in the loop). This is now the simulation, no hardware at risk
	
	Initial goal: launch drone from ground
	Next goal: launch drone, and land
	Third goal: launch drone, hover, movement, etc.
	
	Deliverable for this phase:
	Create a basic video of your simulation drone working. Autonomous takeoff & landing, etc.
	
	

#### Phase 4 - ROS + PX4
	Finally, bring ROS back into the picture.
	ROS → MAVROS → PX4 → Gazebo
	ROS controls the drone now
	
	Deliverable: Autonomous drone flight, with takeoff and landing. Additionally, you can give drone navigation points. For example, go to x, y coordinates and it will land there.
	
	

#### Phase 5 - Computer Vision
	Still no hardware yet, but add a virtual camera in Gazebo and a fake person for it to track.
	
	Get person detection working, and add the drone in for tracking & following the fake person
	
	Deliverable:
  Video of the drone following the simulated person

#### Phase 6 - State Machine
	Implement all states of a drone. NOTE: this is what you are gonna get hired for. Idle, takeoff, search, track, lost, landing, etc.
	
	Deliverable:
  Make a sick architecture diagram


#### Phase 7 - Sensor Fusion
	Combine GPS and camera into one. This way you can estimate the fake human's position through not only vision, but also GPS if it gets lost. Apparently Kalman Filters are useful here
	
	Deliverable:
	Smoother tracking than before

#### Phase 8 - Obstacle Avoidance
	Can't be hitting cars & trees! Spawn in buildings, trees, etc. inside the sim. Have your drone avoid obstacles, both stationary and moving.
	
	Deliverable:
	Drone can navigate through a forest simulation

#### Phase 9 - Real Engineering
	This is where it starts getting real
	1. Write documentation about EVERYTHING!
		1. Architecture diagrams
		2. Requirements
		3. Lessons learned, future work, tradeoffs, cool choices, etc.
	2. Buy hardware
		1. Some used drone on facebook, specifically one that would work with your own software or a pi zero or something.
	3. Fly the drone manually, understand how to get it out of emergency situations
	
	Deliverable:
	Have fun flying a drone, get ready to implement

#### Phase 10 - Drone Autonomy
	Actually implement your code, but one step at a time
	1. Takeoff and landing
	2. Takeoff, hover, landing
	3. Previous + computer vision for tracking
	4. Finally, full obstacle avoidance + GPS
	
