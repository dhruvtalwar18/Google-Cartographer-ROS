# Google-Cartographer-ROS
Final year thesis project on implementation of google cartographer to develop a map of the IIT Delhi campus road using 3D point cloud data. Also to implement localization using the in built cartographer features.Cartographer is a system that provides real-time simultaneous localization and mapping (SLAM) in 2D and 3D across multiple platforms and sensor configurations


<p><img align ="left" src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Test_1/test_1_xy.png" title="Cartographer Map" width = "420" height = "450" ><img align ="right" src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Test_1/Google_img'.png" title="Google Map" width = "375" height = "450" ></p><br><br><br><br><br><br><br><br>
<br><br><br><br><br><br><br><br><br><br><br><br><br>
<p align="center">Fig.1 Map developed by 3D PCL compared to the actual Google map of the area</p><br>
<br><br>


<b><h1>Installation and workspace setup</h1></b>

We shall be using the Google cartographer ROS kinetic package for the same, the installation of the same can be seen <a href="https://google-cartographer-ros.readthedocs.io/en/latest/compilation.html">here </a>

For this we would need rosbags with both "3D point cloud" and "IMU data" using which only we can deploy the package. The package configeration files need to be changed according to the topics we would be using. The following shows what all changes need to be done to get a map. 

<br><br>

<b>Step 1: Creation of a .pbstream file from the ros bag </b>

Since we did not have a proper /tf tree, we decided to use a <a href="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Config_files/backpack_3d.urdf">urdf file</a>  description for providing the frames required by the cartographer. The URDF used by us can be found in the config files folder of the repo. This file was made assuming the dimentions of the Mahindra E20 vehicle, this needs to be modified according to the proper dimentions with proper links. 

We used the launch file test.launch for the first process of generation of .pbstream file. The settings for this launch file were made using insights from the working configurations as uploaded by a user <a href="https://drive.google.com/file/d/0B1KZT92BcdVNaHdkZVp5bkI0WDQ/view?resourcekey=0-n3jnlkSym2P7Hx3RLsqQJw">here</a>

<a href="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Config_files/test.launch">test.launch </a> was made specifically for our use and all the changes made can be seen <a href="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Config_files/Launch_file_edits.docx">here </a>


Once the launch file was ready run the following to generate the pbstream file

$ roslaunch cartographer_ros test.launch bag_filename:=/path/to/your_bag.bag \
<br><br>



<b> Step 2: Creation of maps from the generated .pbstream file </b>

Upon obtaining a .pbstream file, a point cloud file (.ply) can be obtained by running:

$ roslaunch cartographer_ros assets_writer_backpack_4d.launch bag_filenames:=/path/to/your_bag.bag pose_graph_filename:=/path/to/your_bag.pbstream\
The .ply file (along with some image files) will be generated in the same folder as the bag and .pbstream file.

We had created our custom  <a href="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Config_files/assets_writer_backpack_4d.lua">lua file</a> for the generation of the point cloud file, the steps followed can be found <a href="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Config_files/Lua_file_updates.docx">here </a> 
<br>
Once the script was run the respective maps and ply files were successfuly created

<b><h1>Results</h1></b>

The following maps were generated after running the scripts on a <a href="https://drive.google.com/drive/folders/1gcnSY-3-MtDLCSeKLohcuVjIYoow_NfD?usp=sharing">rosbag file </a>, which was created by the E20 vehicle going around the campus.

The blue line shows the trajectory the vehicle took while transversing the campus roads.
<br><br>

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Test_2/combined_test_2.png" title="Cartographer Map, and Google map IIT Delhi Campus, Himadi Circle"></p>

<p align="center">Fig.2 Cartographer Map, and Google map IIT Delhi Campus, Himadi Circle </p>

<br><br>

Some of the other test results are as shown <br><br>

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Other%20tests/output5_2.bag_xray_xy_all.png" title="Cartographer Map Nilgiri Hostel"></p>
<p align="center"> Fig.3 Cartographer Map Nilgiri Hostel </p>
<br><br>


<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Other%20tests/output_6.bag_xray_xy_all.png" title="New Campus Area"></p>
<p align="center"> Fig.3 Cartographer Map New Campus Area </p>

<br><br>

More images of the maps generated can be found out in the images folder uploaded in this repository\
We stiched all the maps together to get the complete path followed by the car on the campus road
<br><br>

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Other%20tests/Full%20map.png" title="Full Campus map "></p>
<p align="center"> Fig.4 Full Campus map </p>
<br><br><br>


<b><h1>Google Cartographer Localization</h1></b>

We also tested Cartographer’s inbuilt localisation package on the bag files for offline
localisation of the car in the 3D maps. The blue coloured trajectories denote the actual
trajectory of the car during the course of the experiment and the green trajectory
represents the output trajectory of the Cartographer localisation package. We were also
able to obtain the coordinates of the points of the trajectory as it is generated along the
way with respect to the map frame.

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Cartographer_localization.gif" title="Cartographer Localization on pre built map "></p>
<p align="center"> Fig. Cartographer Localization on pre built map </p>
<br><br><br>

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/Images/Localization_2.PNG" title="Test Comparison b/w actual and calculated trajectory "></p>
<p align="center"> Fig. Test Comparison b/w actual and calculated trajectory </p>
<br><br><br>



<b><h1>Qt based Sensor Analysis Desktop Application</h1></b>

We built a PyQt5 based sensor data visualization GUI for real-time analysis of various
sensors information. We used GPS coordinates in (Latitude, Longitude) and converted it
into Universal Transverse Mercator (UTM) system coordinates for accurate plotting of
points on Google Map of IIT Delhi Campus. We did the same using utm libraries in Python
and incorporated the Python application with ROS for acquiring the Pixhawk GPS
coordinates and plotting it using a PyQt5 application on a Matplotlib window.In order to analyse the accuracy of the data, we used the Google
Map of the specific parts of the campus set to maximum zoom level as the background tile.
The result of the QT GUI plotter can be seen as below
<br><br>

<p align="center"><img src="https://github.com/dhruvtalwar18/Google-Cartographer-ROS/blob/main/QT_GPS_GUI/QT_Simulation.gif" title="Full Campus map "></p>
<p align="center"> Fig. QT GUI GPS plotter </p>
<br><br><br>







