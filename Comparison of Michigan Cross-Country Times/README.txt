About the problem:
Cross-country in the United States is a distance running sport contested at the high school and college level by both
boys and girls.  Competing athletes run 5,000 meters on a variety of outdoor courses.

As the scope of this task is athletic events in the Ann Arbor, MI area, this is a data analysis of four years of state
championship meet results.  The winning time and mean time for each year are indicated

Why this problem?
As a high school runner myself (and two-time state championship participant for cross-country) I find the subject
to be very interesting, particularly when considering year-over-year data and potential trends in the competition.

About the data:
The data used in this project comes from RunnerSpace's records of the Michigan MHSAA Cross-Country State Championships.
Data from LP, Division 1 was used for all years.

2019:  https://tinyurl.com/tdzx3no
2018:  https://tinyurl.com/tcwsvmk
2017:  https://tinyurl.com/sx7ml4s
2016:  https://tinyurl.com/t44ssls

Visualization:
Please see visualization.png

About the visualization:
The visualization shows three metrics of interest for each year connected by a line graph:
--The winning time for each year
--The mean time for each year out of all runners in the race
--The time needed for a top 25 finish
These values convey to the viewer a few concepts associated with races in general:  How fast would I need to run to win?
How fast would I need to run to place (in this case in the top 25)?  What time would be average for this race?

An important factor in the visualization was how to render the race times.  In the raw data the times are presented in
"stopwatch" format (MM:SS.x), but this is not particularly useful for doing statistical analysis.  In order to get
accurate mean times, the file format value was converted to raw number of seconds.  While this is useful for
calculations, the visualization is clearer with more classic MM:SS rendering of race times, so the labels on the y-axis
are converted back to this format as the visual is created.

One further comment about the y-axis:  traditionally y-axis values start at the bottom with the lowest numbers and
increase up the axis to the maximum value at the top.  However, for this visual the y-axis is reversed so that the
"lowest number" (least amount of race time) is at the top, with "higher numbers" (slower times) at the bottom.  This is
because the eye associates a line graph going up with better performance (such as profits, ratings, population, etc.)
and a graph going down with a decrease in performance or value.  Like golf, running in a sport where a lower raw value
is better, so putting the faster times at the top of the y-axis allows for improved performance to be reflected by an
uptick in the line graph.

Comments:
The data are remarkably similar for each year, with the exception of 2017.  It is likely some conditions (stormy
weather, unreliability of the course, or extreme temperatures) made the 2017 race "slower" as not only the winning time
but the mean and placing times are slower as well.  Year-over-year for 2016, 2018, and 2019 race times are about the
same:  you'd need to be at or around the 15:00 mark to win the race and around 17:00 to be average.
