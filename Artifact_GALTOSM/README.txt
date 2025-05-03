THIS README CONTAINS

1.Structure and content
2.Smoke test requirements
3.Smoke test instructions
4.Reproducible instructions
5.Expected time requierd
6.Resources

1.STRUCTURE AND CONTENT
	The artifact contains
		Model embedding tools
			a.One C++ code
			b.Three python files
		Logic embedding tool
			a. one python file
		
		Test cases
			Which can be fed into GALTOSM tools
			
		Case Studies
			Codes of all reproducable case studies shown in the paper

	Each folder has a README and a READ_DIRECTORY.pdf to guide you through the Artifact directories.

2.SMOKE TEST REQUIREMENTS
	a.CADP VERSION 2024-k "Eindhoven" (version match is mandatory) (https://cadp.inria.fr/)
	b.STORM 1.9.0 (https://www.stormchecker.org/)
	c.Python3
	
	Among the above three CADP requires License(free of cost for academic use). Also the license comes with the IP of the machine so running in a VM might create an issue.

3.SMOKE TEST instructions
	
	The case_study folder contains the .lnt files for reproducing the case studies.

	INSTRUCTION 1 : BUILDING ADTMC using CADP (If you have CADP, if not, skip this and go to the next instruction)
	
		a. Set the environment variables.
				export CADP = location to the cadp folder in your PC (eg. /home/lab/cadp)
				export CADP_BITS = 64
				export CADP_MEMORY = 50000000000
				export PATH = /bin:/usr/bin:/usr/bin/X11:$CADP/com:$CADP/bin.x64

		b. Change directory to
			$BASE_DIRECTORY/Artifact_GALTOSM/case_studies/CADP_case_studies

		c. Choose the case_study you want to test (for say ant_on_a_grid) then chage directory to 
			$BASE_DIRECTORY/Artifact_GALTOSM/case_studies/CADP_case_studies/ant_on_a_grid

		d. Run the command (for say ant on a grid with grid size 8x8)
			time lnt.open ant8.lnt generator ant8.bcg
			OUTPUT : a .bcg(non human readable) file in the same location of .lnt

		e. Run the command
			time bcg_io ant8.bcg ant8.aut
			OUTPUT : a .aut(human readable) file in the same location of .lnt

		f. Run the command
			time sed -i 's/ !/; prob /g' ant8.aut
			OUTPUT : the .aut file's insternal structure change

		g.Run the command
			time bcg_io ant8.aut ant8.bcg
			OUTPUT : a .bcg file in the same location

		h.Run the command
			time bcg_open ant8.bcg evaluator5 ant_property.mcl
			OUTPUT : probability value in the terminal

		In the paper the CADP column time is in t1+t2+t3 where 
			t1 is from step d to step f
			t2 is step g
			t3 is step h

		The .aut file obtained in step (f) has been provided as test case inside the GALTOSM_tool for all case studies.

	INSTRUCTION 2 : Convert the model (ADTMC(.aut) to SDTMC(.tra .lab))

		There are two possible location($AUT_LOC) of .aut file(ADTMC)
			1. If you followed INSTRUCTION 1(i.e. if you have CADP) then the location of .aut file is
				$BASE_DIRECTORY/Artifact_GALTOSM/case_studies/CADP_case_studies/ant_on_a_grid (for say we are doing for ant on a grid)

			2. If CADP is not present we have provided the .aut files in the location
				$BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/test_cases/adtmc_to_sdtmc
				
				we have provided the log.txt file in the location $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/CADP_case_studies/log_files_for_cadp
				to establish the sanctity of the .aut creation.

		a. Change directory to
			$BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/adtmc_to_sdtmc-dev/build

		b. RUN THE COMMAND
			./ADTMC_TO_SDTMC $AUT_LOC -STORM

			replace the $AUT_LOC with the proper location of the .aut file(As discusseed above).
			OUTPUT : .tra and .lab will get created in the $AUT_LOC which is our SDTMC

	INSTRUCTION 3 : Convert APCTL specification to PCTL specification

		Command for all 4 logics for each case study has been given, choose as per your choice

		a. Change directory to 
			$BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/logic_translator_tool
		
		b.LOGIC of ant_on_a_grid:
			Run the command
				python3 logic_translator.py APCTL "(P=?[(true)_(true)U_(\"LIVE\")(true)])"

				perserve the output logic displayed on terminal which will be used for model checking
			
		b.LOGIC of lost_boarding_pass:
			Run the command
				python3 logic_translator.py APCTL "(P=?[(true)_(true)U_(\"LAST_GOT_SEAT\")(true)])"

				perserve the output logic displayed on terminal which will be used for model checking

		b.LOGIC of bounded_retransmission_protocol:
			Run the command
				python3 logic_translator.py APCTL "(P=?[(true)_(\"ATTEMPT\" | \"SUCCESS_FRAME\" | \"ACK_FAIL\" | \"RETRY1\" | \"RETRY2\")U_(\"SUCCESS_FILE\")(true)])"

				perserve the output logic displayed on terminal which will be used for model checking

		b.LOGIC of gambling problem:
			Run the command
				python3 logic_translator.py APCTL "(P=?[(true)_(true)U_(\"HOME\" | \"DRUNK\")(true)])"

				perserve the output logic displayed on terminal which will be used for model checking


	INSTRUCTION 4 : Model check using STORM model checker

		NOTE:
			Depending upon your CADP availability the $AUT_LOC has the SDTMC(.tra .lab)
			So the $AUT_LOC is having the SDTMC

			Make sure STORM is installed

		a. Change directory to /home/user/storm-stable/build/bin

		b. Run the command (for ant on a grid)
			./storm --explicit $AUT_LOC/ant8.tra $AUT_LOC/ant8.lab --prop "(P=?[((\"bot\"&(true))|(!(\"bot\")&(true)))U((!(\"bot\")&(\"LIVE\"))&P>=1[X(\"bot\"&(true))])])"
		b.  ./storm --explicit $AUT_LOC/bp_102.tra $AUT_LOC/bp_102.lab --prop "(P=?[((\"bot\"&(true))|(!(\"bot\")&(true)))U((!(\"bot\")&(\"LAST_GOT_SEAT\"))&P>=1[X(\"bot\"&(true))])])"
		b.  ./storm --explicit $AUT_LOC/brp_10_101.tra $AUT_LOC/brp_10_101.lab --prop "(P=?[((\"bot\"&(true))|(!(\"bot\")&(true)))U((!(\"bot\")&(\"LIVE\"))&P>=1[X(\"bot\"&(true))])])"
		b.  ./storm --explicit $AUT_LOC/gamble_3_105.tra $AUT_LOC/gamble_3_105.lab --prop "(P=?[(("bot"&(true))|(!("bot")&(true)))U((!("bot")&("HOME" | "DRUNK"))&P>=1[X("bot"&(true))])])"

4.REPRODUCIBILITY

	GALTOSM Consists of the following converters

		a. CADP -> STORM or PRISM (ADTMC to SDTMC)
			source code location : $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/adtmc_to_sdtmc-dev
			for verification : Go through the steps in the README.txt of location $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/test_cases/adtmc_to_sdtmc

		b. mcrl2 ->	STORM or PRISM (ADTMC to SDTMC)
			source code location : $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/adtmc-mcrl2_to_sdtmc-prism
			for verification : Go through the steps in the README.txt of location $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/test_cases/adtmc-mcrl2_to_sdtmc-prism

		c. PRISM -> .mcrl2
			source code location : $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/sdtmc_to_adtmc
			for verification : Go through the steps in the README.txt of location $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/test_cases/

		d. PRISM -> .aut(of CADP format)
			source code location : $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/model_translator_tool/sdtmc_to_adtmc
			for verification : Go through the steps in the README.txt of location $BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/test_cases/

		e. Rewad based model checking of an converted SDTMC
			for verification : Go through the README.txt of the location $BASE_DIRECTORY/Artifact_GALTOSM/case_studies/reward_based_SDTMC

5.EXPECTED TIME REQUIRED
	For expected requirement one can see the time mentioned in tables of the paper under case study section and in the GALTOSM_handbook section are in similar range. Because with respect to the size of the case study, the will vary. So the time requirement is completly dependent which case study example is chosen.
	Minimum time : ~1 minute
	Maximum time : ~25 hours(for a single case instance of a case_study)
	This time estimation is on the assumption that the machine configuration is same as mentiones below.

	For the range of case studies, choosing a case study from the lesser half would take lower time(few minutes).

6.RESOURCES
	
	All of these case studies has been performed on workstation having
		a. Intel® Xeon(R) Silver 4314 CPU @ 2.40GHz × 64
		b. 640.0 GB RAM
		c. 1TB SSD
		d. Ubuntu 22.04.5 LTS
