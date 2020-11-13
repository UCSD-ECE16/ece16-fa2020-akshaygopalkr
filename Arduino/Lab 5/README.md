# Arduino Code for Lab 5

## Summary 
> The Arduino Code we used in this lab was very similar to what 
> we used in Lab 4 and Lab 3. We used parts of the TutorialPlottingWearable 
> to sample acceleration values at 50 Hz. One feature that we added 
> was to display the step count we calculate in the Python challenge files. From 
> the Python code, we sent a message that contained the number of steps. Using this 
> else-if block, we would display this message on the LED Display.  

     else if(command != "")
     {
        writeDisplay(command.c_str(), 0, true);
     }