FOLDER DETAIL
____________________________

This folder contains
	1) The CPP files of the ADTMC to SDTMC model translator.
	2) The build folder contains the executable.
	3) GENERATE_EXECUTABLE.sh builds the executable automatically

HOW TO BULD EXECUTABLE:(if not alredy build)
______________________________

One can still remove the build directory and follow the below steps:

Prerequisite
-------------
	1) cmake 3.1 or higher 
	(https://askubuntu.com/questions/610291/how-to-install-cmake-3-2-on-ubuntu)
	for upgradation or installation
	
	2) C++
	


METHOD1:(automated)
-------------------
	1) RUN THE COMMAND
			source GENERATE_EXECUTABLE.sh

METHOD2:(manual)
-------------------
STEPS:
	1) make a folder named `build' (create if not created alredy)
	2) change directory to build
	3) RUN THE COMMAND
		cmake ..
	4) RUN THE COMMAND
		cmake --build .

	OUTPUT:
		A executable will get created with the name 'ADTMC_TO_SDTMC' which is the model translator tool to convert ADTMC to SDTMC by taking input of .aut file and generate .lab and .tra files.
