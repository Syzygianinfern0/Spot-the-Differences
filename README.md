# Spot-the-Differences
Displays differences between pictures on a LED matrix. 
Task 0 of my Spider Inductions for the Summer of '19
### Youtube Link
Here you go : [Bear the Cringe 🤣](https://www.youtube.com/watch?v=W3XFHgI8PFY)
### Code Stack
* Embedded C - Processor Control in a Register-wise manner
* OpenCV - Image manipulations 
* Numpy - Computations
* Serial - Interface for Python to communuicate with Arduino
### Instructions
1. Make a 6x6 matrix 😂 and connect anodes to D2-7, cathodes to B0-5
2. Upload `display/display.ino` to your UNO
3. Run the `Spot the Differences.py` and tune the Parameters to your liking
4. Press ESC hard
5. U have the matrix lighting Up!!
# Problem Statement 
One day, you find an interesting puzzle on a magazine, asking to find as many differences between two given images for an astounding prize money. You being lazy, despite the reward, want to find a simple yet robust algorithm which can do the given task with good accuracy. Finally, you go a step ahead and make an LED matrix of suitable size, segment the image into corresponding size and glow the LED's wherever you find a difference with the help of a microcontroller.
# Results
![cv](Results/Result.png)
<br>
![matrix](Results/Matrix.png)
