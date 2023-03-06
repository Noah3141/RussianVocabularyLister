from vocablib.utils.ProgressBar import ProgressBar
import time

### NOTE you must have "progressbar2" installed in your python environment ###

# EXAMPLE USING "progress increment"
progress = ProgressBar()


num_steps = 12
progress.start(num_steps, "Calculating X Cases")  # progress bar is set for a width (duration) of 12 steps

num_cases = 6
for i_case in range(num_cases):
    time.sleep(1)  # Sleep for 1 second
    progress.increment(2)    # increment the progress by 2 steps (i.e. 2 steps per case to get to 12 steps)
progress.finish()    # Finish the progress bar


# EXAMPLE USING "progress update"
# In this example, the progress is set for 100 steps (and will sleep 100 milliseconds on each step)
# but upon getting to step x (x% of total looping), we will jump directly to being y% complete and then finish there.

num_cases = 100
x = 40
y = 80

progress.start(num_cases, "Updating Example")  # progress bar is set for a width (duration) of 12 steps
for i_case in range(num_cases):
    if i_case == x:
        progress.update(y)
        break
    time.sleep(.1)  # Sleep for 1 second
    progress.increment(1) # increment the progress by 1 step
    pass

progress.finish()    # Finish the progress bar




# Note that the following form of specifying a number using underscores can be used to make large numbers more readable.
#  The underscore represents a comma. It is ignored by the python compiler -- it's only for human assistance.
#   so the number "100,000" can be written in python as "100000" or as ""100_000"
num_cases = 100_000
