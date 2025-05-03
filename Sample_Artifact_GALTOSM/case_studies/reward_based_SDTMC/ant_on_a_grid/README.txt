FOLDER DETAILS
______________________________

This folder contains Reward based SDTMC with reward in the state.
And a logic file in PRCTL




HOW TO RUN(model check on reward based property):
_________________________________________________

STEPS:
	1) Make sure STORM(https://www.stormchecker.org/) is installed in the system.
	
	2) change directory to storm executable
		/home/storm-stable/build/bin
	
	3) RUN THE COMMAND (for reward based model checking)
		./storm --explicit $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/ant_on_a_grid/ant32.tra $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/ant_on_a_grid/ant32.lab --staterew $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/ant_on_a_grid/ant32.srew --prop $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/ant_on_a_grid/aog_p.props
