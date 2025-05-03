FOLDER DETAILS
________________________

This folder contains two SDTMCs in the form of (.sta .lab .tra)




HOW TO RUN:
____________

STEPS:
------
	1) change directory to 
		$BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/sdtmc_to_adtmc
		
	If you want mcrl2 code follow step 2.
	If you want .aut(CADP compatible) follow step 3)
	
	2) python3 sdtmc_to_mcrl2.py <path_to_sta> <path_to_lab> <path_to_tra>
	
	3) python3 sdtmc_to_cadp.py <path_to_sta> <path_to_lab> <path_to_tra>
	
OUTPUT:
-------
	The outputs will be generated in the same location as of the SDTMCs.
