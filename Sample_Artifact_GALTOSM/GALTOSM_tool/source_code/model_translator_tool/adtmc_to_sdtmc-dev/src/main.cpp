#include <iostream>
#include <string>

#include "aut.hpp"


void print_help()
{
    std::cout << "This command line utility converts .aut files (ADTMC) to\n"\
              << "STORM or PRISM files (SDTMC).\n\n"\
              << "    adtmc_to_sdtmc model.aut <-PRIM|-STORM>\n\n"\
              << "Either of -PRISM or -STORM is required in input. The model is\n"\
              << "embedded to a equivalent State Labelled Discrete Time Markov Chain"
              << std::endl;
}


int main(int argc, char** argv)
{
    if (std::string(argv[argc-1]) == "-help" || argc != 3)
    {
        print_help();
        return 0;
    }

    std::string fname(argv[1]);
    bool storm;
    if (std::string(argv[2]) == "-PRISM")
        storm = false;
    else if (std::string(argv[2]) == "-STORM")
        storm = true;
    else
    {
        print_help();
        return -1;
    }

    Aut* aut = read_aut_file(fname);

    if (aut == nullptr)
    {
        std::cout << "Unable to read .aut file specified" << std::endl;
        return -1;
    }

    std::string fname_no_ext = fname.substr(0, fname.find_last_of('.'));


    if (!aut_convert(aut, fname_no_ext + ".lab", fname_no_ext + ".tra", storm))
    {
        std::cout << "Unable to write .lab or .tra files" << std::endl;
        delete aut;
        return 0;
    }

    delete aut;
}