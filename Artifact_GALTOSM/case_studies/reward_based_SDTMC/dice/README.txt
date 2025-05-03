FOLDER DETAILS
______________________________

This folder contains Reward based SDTMC with rewarsa in the state.
And a logic file in PRCTL




HOW TO RUN(model check on reward based property):
_________________________________________________

STEPS:
	1) Make sure STORM(https://www.stormchecker.org/) is installed in the system.
	
	2) change directory to storm executable
		/home/storm-stable/build/bin
	
	3) RUN THE COMMAND (for reward based model checking)
		./storm --explicit $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/dice/dice_adtmc.tra   $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/dice/dice_adtmc.lab   --staterew   $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/dice/dice_adtmc.srew   --prop $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/dice/dice_p.props
