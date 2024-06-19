# :test_tube: PsyTestPro

PsyTestPro is a Python program developed using the Pygame library that allows users to create and manage experiments.
With PsyTestPro, users can define suites, each of which consists of a series of tasks. These tasks can be
customized to suit specific requirements.

The user interface of PsyTestPro is intentionally designed to be predominantly black. This deliberate choice is driven
by its primary application in sleep studies. By minimizing light emission, PsyTestPro ensures a conducive environment
for conducting experiments, where even the slightest disruptions from external sources of light are mitigated.

## :gem: Key Features

### :microscope: Suite Creation:

Users can easily create suites by specifying the tasks they want to include and setting up a schedule for when each
task should be executed.

### :wrench: Customizable Tasks:

For each task within a suite, users have the flexibility to select their own scripts, allowing for a wide range of
experimental designs and functionalities.

### :calendar: Schedule Management:

PsyTestPro provides a scheduling system that displays the upcoming tasks and their respective execution times. This
allows users to have a clear overview of the experiment's timeline.

### :rocket: Automated Execution:

Once a suite is started, PsyTestPro will automatically manage the execution of tasks according to the predefined
schedule. When a task's scheduled time arrives, PsyTestPro will launch the corresponding script.

## :books: Table of Contents

- [:test\_tube: PsyTestPro](#test_tube-psytestpro)
  - [:gem: Key Features](#gem-key-features)
    - [:microscope: Suite Creation:](#microscope-experiment-creation)
    - [:wrench: Customizable Tasks:](#wrench-customizable-tasks)
    - [:calendar: Schedule Management:](#calendar-schedule-management)
    - [:rocket: Automated Execution:](#rocket-automated-execution)
  - [:books: Table of Contents](#books-table-of-contents)
  - [:inbox\_tray: Installation](#inbox_tray-installation)
  - [:arrow\_forward: How to run PsyTestPro](#arrow_forward-how-to-run-psytestpro)
    - [:gear: Start Settings](#gear-start-settings)
    - [:clock1: Schedule](#clock1-schedule)
    - [:running: Run tasks](#running-run-tasks)
  - [:nut\_and\_bolt: Configure PsyTestPro](#nut_and_bolt-configure-psytestpro)
    - [:heavy\_plus\_sign: Create suite](#heavy_plus_sign-create-experiment)
    - [:x: Delete experiment](#x-delete-experiment)
    - [:heavy\_plus\_sign: Add Task](#heavy_plus_sign-add-task)
      - [Variables](#variables)
    - [:x: Delete task](#x-delete-task)
    - [:heavy\_plus\_sign: Create Custom Variables](#heavy_plus_sign-create-custom-variables)
    - [:outbox\_tray: Export experiments](#outbox_tray-export-experiments)
    - [:inbox\_tray: Import experiments](#inbox_tray-import-experiments)
  - [Citation](#citation)
  - [:question: FAQ](#question-faq)

## :inbox_tray: Installation

To install PsyTestPro you can either download this GitHub project as a ZIP and unpack it, or you can clone the
repository using git:

```git
git clone https://github.com/eliasmattern/PsyTestPro
```

To use PsyTestPro python must be installed:
[Download here](https://www.python.org/downloads/)

There are also some dependencies that must be installed using pip:

```python
pip install pygame
pip install pandas
pip install openpyxl
pip install pygame_widgets # optional (Required by chronobiology basel tasks )
```

## :arrow_forward: How to run PsyTestPro

To start PsyTestPro simply execute the `psytestpro.py` in the root directory.

### :gear: Start Settings

To start an experiment, and its schedule, you have to put in the following values:
| Name | Description |
| ------------- | ------------- |
| Participant ID | Name of Participant |
| Experiment | Name of experiment |
| Start Time | Time, when the experiment should start |

When everything is filled out correctly, you can press submit.

### :clock1: Schedule

After you start an experiment, you will see a table with all the tasks, their start time and state. There you can modify
to each task.

You can change the Date, Time and State. The State shows if a Task is todo, should be skipped, or is done.

### :running: Run tasks

Use the button `Run Experiment` to start the PsyTestPro with your schedule.
When it starts, there will be a timer until the next Task. When it reaches 0 it
plays the task and sets it to `done`.

You can always press `Play next task` to start the next task without waiting for the timer to run out.

If a task takes longer than expected and another task should have already started, it will be executed as soon as the
previous task is finished.

## :nut_and_bolt: Configure PsyTestPro

To set up a suite, you will have to go to `Configure Test Battery`.
From there, you can do the following actions:

- Create Suite
- Delete Suite
- Create task
- Delete task
- Create Custom Variables
- Delete Custom Variables
- Import experiments
- Export experiments

### :heavy_plus_sign: Create suite

The suites you create will have a schedule with tasks for the user. You can also declare that an suite should
not have a schedule. If you do this, all tasks will immediately start when PsyTestPro begins.

### :x: Delete suite

Here you can delete your suites. Once deleted, the suite and its tasks will be removed.

### :heavy_plus_sign: Add Task

A task can be a screen with text, your own script or an URL. To create a task, you have to assign a name and a task duration.

Task properties

| Name          | Description                         |
|---------------|-------------------------------------|
| Name          | Name of the task                    |
| Task duration | Time a task takes.                  |
| Command       | Command to execute your own script* |
| Title         | Title of the screen with text       |
| Description   | Description of the screen with text |
| url           | URL to a Webpage                    |

> <p style="color: #d7ba7d; font-size: 0.8em; line-height: 1.1em;">
> * Use relative paths instead of absolute paths to execute a file. <br /> 
> A relative path starts in the directory you are in. An absolute path has the entire file path. This can be a problem when you use the schedule on a different computer. <br />
>Example: <br />
 >C:\users\[username]\Desktop\psytestpro\scripts\your_own.script <br />
 >Because of the username in your path, it will only work on your computer. <br>
 >Instead use: <br />
 >.\scripts\your_own.script <br />
 >This will go from the PsyTestPro folder into the script folder to access your script. 
 >Therefore, it would work on any computer which has the script at this location.</p>

#### Variables

If you want to provide your command or text screen some variables, you can choose from the variables below. These will
have the value you provide when you start a suite

| Usage         | Description                                                                                                  |
|---------------|--------------------------------------------------------------------------------------------------------------|
| {id}          | Participant ID                                                                                               |
| {suite}       | Suite Name                                                                                                   |
| {startTime}   | Time when the suite started                                                                                  |
| {timestamp}   | Current time stamp. Format: YYYY.mm.dd hh:mm:ss                                                              |
| {scriptCount} | A counter that increments with each execution of the command within a task (used only for commands and urls) |

> NOTE: The preview will use an example text ("VARIABLE") not the actual value because no suite will be selected at
this moment.

Example command:
py yourTask.py {suite}

Before you save a task, use the preview to see if everything is working.

### :x: Delete task

Here, you can delete tasks from suites. Once deleted, the task will be removed.

### :heavy_plus_sign: Create Custom Variables

Here you can create custom variables. You can use them like the other variables:

Usage: ```{CustomVariableName}```

For each variable, an input box will be created on the start page of PsyTestPro

<strong>What are custom variables good for? </strong><br />
To provide specific information in your script, perhaps to save data, you can provide this information with a custom
variable. In your code, you need to figure out how to access command line arguments, and then you can use them in your
code.

Example command of a task: ```python ./path/to/your_script.py {CustomVariableName}```

### :outbox_tray: Export Test Battery

This will export all your suites, their tasks and schedule.
It will create a CSV in the `./exports/` folder.
You can use this CSV to Import the suite again.
><p style="color: #CC7F7F; font-size: 0.8em; line-height: 1.1em;">
>NOTE: This will not export your own scripts. You will have to transfer these by yourself.</p>

### :inbox_tray: Import Test Battery

This allows you to choose a CSV on your computer to import Suites and their tasks

## Citation

Use the following to cite PsyTestPro:
Mattern, E., Capdevila, N., & Lane, L. PsyTestPro [Computer software]. https://github.com/eliasmattern/PsyTestPro

## :question: FAQ

<strong>What scripts are supported?</strong><br /> Any scripts, which you can execute from the console are supported by
PsyTestPro

<strong>I found a bug/problem. How can I report it?</strong><br />
You are welcome to create an Issue [here](https://github.com/eliasmattern/psytestpro/issues)

<strong>How can I contribute?</strong><br />
Yes, you can! Follow these steps to find out how: [here](./information/contribute.md)
