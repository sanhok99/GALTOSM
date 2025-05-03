FOLDER DETAILS
______________________________

This folder contains a logic file in PRCTL.
And reward based SDTMC with two different rewarding structure in the state.

r1 : where reward has been given to GAMBLE and SIT states (10.39284735)

r2 : where reward has been given to GAMBLE and NOT_SIT states (20.76490868)


STEPS:
	1) Make sure STORM(https://www.stormchecker.org/) is installed in the system.
	
	2) change directory to storm executable
		/home/storm-stable/build/bin
	
	3) RUN THE COMMAND (for reward based model checking based of r1 reward stucture)
		./storm --explicit $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102.tra $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102.lab --staterew $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102_r1.srew --prop $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_p.props 
		
		
	4) RUN THE COMMAND (for reward based model checking based of r2 reward stucture)
		./storm --explicit $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102.tra $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102.lab --staterew $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_2_102_r2.srew --prop $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC/gambling_problem/gamble_p.props 
Storm 1.9.0

