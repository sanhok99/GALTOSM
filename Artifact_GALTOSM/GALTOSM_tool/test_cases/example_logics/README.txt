FOLDER DETAIL
____________________________

This folder contains
	1) example_logics.txt
		which has example of logic of the below 6 types
			a) APCTL
			b) APCTL star
			c) APCTL with rewards
			d) PCTL
			e) PCTL star
			f) PCTL with rewards
		For each logic the semantics and the command line input form, both has been provided.
		
	2) run_LogicTranslator.sh
		This file contains the shell code which will convert all the example logics using
		the logic translator tool of GALTOSM
		
		
		
HOW TO RUN(translate any logic):
________________________________

METHOD 1: (automated)
---------------------
RUN THE COMMAND

source run_LogicTranslator.sh

METHOD 2:(manual)
-----------------
STEPS:

	1) Move to the directory
		$BASE_DIRECTORY/Artifact_GALTOSM/GALTOSM_tool/source_code/logic_translator_tool
		
	2) RUN THE COMMAND
		python3 logic_translator.py <input_logic_type> "input_logic"
		
	  Replce the input_logic with a synticatally correct logic available in example_logic.txt file.
	  Replce the input_logic_type with the type of the logic
	  (APCTL | APCTLS | APRCTL | PCTL | PCTLS | PRCTL).
	  
	  The Converted logic will be displayed in the terminal.
	  
	3) If the property needs to be stored in a file run the command
		python3 logic_translator.py <input_logic_type> "input_logic" >o.props
		

