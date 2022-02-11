# Grab x Pulis

Detailed analysis done to investigate possible reasons for delay in Grab services for NUS Data Analytics Competition 2022, to be found in [here](https://github.com/kenghweeng/Grab_The_Pulis/blob/main/final.ipynb) and [here](https://github.com/kenghweeng/Grab_The_Pulis/blob/main/Analyze_Jakarta_Routes.ipynb).

Our main tech-stack:
* Vahalla, a C++ implementation for map matching.
* ipyleaflet, for very interactive visualizations of geospatial data analysis
* geopandas
* Dask
* matplotlib & seaborn

We've shortlisted the reasons to be:
* Traffic bottlenecks at popular shopping malls due to narrow infrastructures of pickup points. We comparatively found out that pickup speeds at Changi Airport with optimized pick-up and drop-off pioints are much faster at the initial and end-timings of each trip, compared to popular shopping malls with narrow queues at their pick-up and drop-off locations. <br>
![image](https://user-images.githubusercontent.com/16697123/153622574-8d30dd89-6626-4ce8-832b-97c49b942035.png)

* Drivers picking inefficient routes, as we compare the actual driver routes taken with popular Google Maps and Open Street Map routes which we pulled using Google Maps API and `osmnx`. We found out that drivers's supposed "shortcuts" are more often slower, albeit, there were in-fact expert-curated routes which were actually even faster than Google Maps and Open Street Maps. These insights could be used to augment Grab-Nav!

Team Leads: Keng Hwee @kenghweeng <br>
Team Members: 
* Russell Saerang @RussellDash332
* Sean Gee Zhing @pikasean
* Terry Lim @terrylimxc
* Jonathan Chen @cysjonathan
