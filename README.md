# Graphic DronePi
### Collecting Atmospheric Pollution and Emission Data Utilizing a Raspberry Pi computer on a Hexacopter Drone

![David and Saleh determining the best placement for the Raspberry Pi on the drone](https://i.imgur.com/7DZwYuq.jpg)
<center><i>Image 1. Engineering student David, and Computer Science professor Saleh determining the best placement for the Raspberry Pi on the drone.</i></center>

---

This is a collaborative undergraduate research project between students from the University of Wisconsin - Fox Valley and the University of Wisconsin - Stout

#### General Paper Abstract
Federal and state environmental agencies delegate industries the responsibility to maintain a permissible level of pollution in the environment. Multicopter drones offer scientists and engineers a flexible and creative solution to collect and analyze atmospheric pollution data. Drones are a popular, cost-efficient tool that can be customized for data collection in several fields of study. Utilizing such drones can offer cities, manufacturing plants, and regulatory bodies a solution to monitor environmental compliance and affordably measure the concentration of selected gases within a predefined geospatial area. Modular construction of interchangeable components provides the flexibility to customize sensor packages based on what pollutant is to be targeted for detection. The design and construction of a custom-built drone is described here, where a headless Raspberry Pi 3B+ single-board computer and various gas and GPS sensors are mounted on to a human-controlled hexacopter drone. Software is designed to automate the collection of readings, allowing the pilot to only concentrate on the flight of the drone. The SSH network protocol allows the Raspberry Pi to be controlled remotely from the ground if desired. LED bulbs mounted on the airframe additionally provide instant feedback of the drone's status. Results recorded from tests are collected post-flight and are plotted graphically for analysis.


#### Graphical Representation
The main purpose of the drone is to manage a way to help data scientists find solutions to collect controlled, consistent, repeatable data in areas that can be difficult to attain, such as high (legal altitudes). The neat caveat is that this does not strictly need to be limited to atmospheric sciences, although its bes uses may be found there. Flying a drone headless (no visual display of seeing what the Raspberry Pi is doing) can be cumbersome, particularly when the LEDs become too difficult to tell if they are illuminating. That is why this script also comes with a curses graphical representation. Bar graphs are drawn to any reasonable sized console window, with the temperature printed on the left and the humidity printed on the right. By default, the temperature's bargraph will print anywhere between 20 to 40 degrees Celsius, and the humidity's bargraph will print anywhere between 0 to 100%. Trivial statistics will print in the middle of the screen

![As the drone rests, the Raspberry Pi runs the software](https://i.imgur.com/ZKuuN9p.jpg)
<center><i>Image 2. As the drone rests, the Raspberry Pi runs the software, writing the raw data to a text file for later use and drawing the data onto the console window using the curses framework.</i></center>

---

## Presentations, Publications, and Awards
#### MICS 2019
Several presentations at notable events have been made to display this drone. The group was selected to have their [research paper accepted and published](http://www.micsymposium.org/mics2019/wp-content/uploads/2019/05/Drone_FV__submitted_.pdf), and was allowed the honor of presenting their work at [the 2019 Midwest Instruction and Computing Symposium](http://www.micsymposium.org/mics2019/) held at North Dakota State University in Fargo, North Dakota on April 5th, 2019.

#### 2019 System Symposium

David and Eric was also accepted to [present their research at the UW System Symposium for Undergraduate Research and Creative Activity](https://uwosh.edu/today/73781/student-faculty-research-teams-offer-results-from-chemistry-projects-and-more-at-uw-system-symposium/) on Friday April 26th, 2019. This event was a poster symposium for many University of Wisconsin students to present their findings.

![David and Eric perform live demonstrations of the drone and Raspberry Pi](https://i.imgur.com/zgyqgTW.jpg)
<center><i>Image 3. David and Eric perform live demonstrations of the drone, booting the Raspberry Pi and collecting the rather uninteresting temperature and humidity of the room.</i></center>

#### 2019 UW System Research in the Rotunda

Eric made a lone presentation of the drone in the Wisconsin State Capitol building at the [16th annual UW System Research in the Rotunda](https://www.wisconsin.edu/news/archive/uw-system-undergraduates-showcase-research-in-capitol-rotunda-in-16th-annual-event/), a prestigious event where students present their research to their local state representatives, legislators, and the press, explaining directly why their research matters and why their funding, support, and their investment in education matters.

![Presenting at the Wisconsin State Capitol Building.](https://i.imgur.com/HU7QMuI.jpg)
<center><i>Image 4. Presenting at the Wisconsin State Capitol Building. The drone has captured the interest of Ray Cross, the President of the University of Wisconsin System. Eric takes on questions regarding how business can benefit from this drone as well for emissions compliance as well.</i></center>

#### IEEE EIT 2019
The final paper regarding this drone as we worked on it was accepted and published by Institute of Electrical and Electronics Engineers (IEEE), for the International Conference on Electro Information Technology (EIT). The [full publication can be found here](https://ieeexplore.ieee.org/document/8833975), <i>(DOI: 10.1109/EIT.2019.8833975)</i> however IEEE text is behind a paywall without an account. Unfortunately the conference was held in Brookings, South Dakota during the same day as Eric's graduation from UW Fox Valley, and he could not attend.

---

#### Contact the Author
Should you wish to contact me for any suggestions, improvements, or comments, you can use GitHub's `@McDanielES` mention system to contact me. I will try to respond as soon as I am available.
I am a second-year computer science student at the University of Wisconsin - Fox Valley. I am learning the fundamentals of programming in Java, Visual Basic.NET, Python, and C++. This program was written primarily for my benefit and to apply the skills learned in class into a real-world context. I am aware that it may not be realistic and often crude or unsophisticated. But <i>live and learn.</i>
You are free to clone, fork, modify and use this application as you please.
