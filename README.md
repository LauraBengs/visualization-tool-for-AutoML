# visualization-tool-for-AutoML
This is the github repository for my bachelor thesis "Development of a visualization tool for AutoML to increase user trust and understanding", where I investigated the question "How can a visualization tool increase trust in AutoML systems and does it help users to better understand AutoML processes?".

![image](https://github.com/user-attachments/assets/c426ef4a-76c6-42e5-bbce-a8067de6a566)

## Abstract
As the machine learning process is tedious and complex even for experts, Automated Machine Learning (AutoML) is constantly gaining importance and holds high promises to open up the field of machine learning to non machine learning experts. On the other hand, AutoML systems are recurrently unable to provide users with information about the process, making it impossible for the user to understand what is going on during calculations. This missing transparency leads to a lack of user trust and might be a major hindrance for large scale adaption of AutoML. By enabling the user to follow along the process a higher user acceptance and wider application of AutoML systems could be achieved. This thesis makes the following contributions: 1) A visualization tool for AutoML was developed, representing the AutoML process through a directed acyclic graph and its visual attributes. Thereby, the tool is interactive, autonomous and optimizer-agnostic. 2) The tool was evaluated in a subsequent online user survey, whereby the following results were found: The representation as a directed acyclic graph led to improved user understanding and increased users response speed as well as a significant positive impact on user trust and satisfaction was recognized.

## Features
- Ability to select a run, upload a JSON file of the run, configure the visualization (e.g., specify a threshold, choose a evaluation measure) in the run section
- Visualization as directed acyclic graph, where AutoML search runs are illustrated by visual attributes (e.g. edge thickness, node color)
- Current best solution is visible at first glance
- Interactivity through control bar, buttons, and modals that open when a node is clicked
- Two additional visualizations: anytime performance plot, parallel categories plot

## Future work and open issues
- Enable ad-hoc analysis
- Extend the tool to display more complex solution candidates
- Implement a scale (or traffic light?) that indicates how well the current best solution is performing (e.g., Does this solution meet previously defined requirements? Is there a high probability that a better performing candidate exists?)
