FOLDER DETAIL
____________________________
This folder contains the ADTMC in the form of the .aut files.

For all the case studies presented in the paper, that are 
1) Ant on a Grid (ant$SIZE_OF_GRID)
2) Lost boarding pass problem (bp_$NUMBER_OF_PASSENGERS)
3) Bounded Retransmission Protocol (brp_$NO_OF_RETRY_$NO_OF_FRAME)
4) Gambling problem(gamble_$NO_OF_GAME_$TARGET_AMOUNT)

We have provided the files which are not too large.

These files acts as INPUT to the GALTOSM's model translator tool to convert an ADTMC to a SDTMC.



HOW TO RUN(CONVERT ADTMC TO SDTMC):
______________________________

METHOD 1(automated)
----------
We have provided RUN_TEST_CASE.sh file which takes two arguments,
1)filename.aut
2)OUTPUT FORMAT
	 2.1) -PRISM for prism file types
	 2.2) -STORM for storm file types

Run the command:
source RUN_TEST_CASE.sh <filename>.aut -STORM 
(OR)
source RUN_TEST_CASE.sh <filename>.aut -PRISM 


Choose the file you want to enter and give the corresponding name in <filename>.

OUTPUT:
Two files will get created in the same(as of .aut location) location with filenames <filename>.tra and <filename>.lab


METHOD 2(manual)
---------
To run the model translator manually, follow the steps,

We consider the location where you keep the Artifact to be $BASE_LOC,

1) change directory to $BASE_LOC/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/adtmc_to_sdtmc-dev/build

2) RUN THE COMMAND
	 ./ADTMC_TO_SDTMC $BASE_LOC/Artifact_GALTOSM/GALTOSM_tool/test_cases/adtmc_to_sdtmc/<filename>.aut -STORM
(OR)
	./ADTMC_TO_SDTMC $BASE_LOC/Artifact_GALTOSM/GALTOSM_tool/test_cases/adtmc_to_sdtmc/<filename>.aut -PRISM

OUTPUT:
Two files will get created in the same(as of .aut location) location with filenames <filename>.tra and <filename>.lab


NOTE: These .lab .tra files can be used in the case_study recreation.
