FOLDER DETAILS
_______________

This folder contans two python source code for converting SDTMC to ADTMC

FILE 1: sdtmc_to_cadp.py
	This file takes input a PRISM generated SDTMC in form of three files(.sta .lab .tra) and produces a .aut file which is compatible to CADP model checking
	
	
FILE 2: sdtmc_to_mcrl2.py
	This file take  input a PRISM generated SDTMC in form of three files(.sta .lab .tra) and produces a .mcrl2 code which is a source code for the Action based model checker mcrl2.
	
	Form this .mcrl2, the following commands can be used to compile the model
		i) mcrl22lps
		ii) lps2lts look more in (https://www.mcrl2.org/web/user_manual/tools/tools.html)
