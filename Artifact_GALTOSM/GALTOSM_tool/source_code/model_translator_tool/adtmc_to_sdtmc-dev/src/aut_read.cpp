#include "aut.hpp"

#include "mio/mio.hpp"

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>

static const std::string NUMERIC_CHARS = "0123456789.";

static bool parse_des(std::istringstream& fss, AutDes& des)
{
    if (fss.ignore(5, '(') &&
        fss >> des.init_state &&
        fss.ignore(2, ',') &&
        fss >> des.num_trans &&
        fss.ignore(2, ',') &&
        fss >> des.num_states &&
        fss.ignore(2, ')'))
    {
        std::string tmp;
        std::getline(fss, tmp);
        return true;
    }
    return false;
}

static bool parse_trans(std::istringstream& fss, std::vector<AutTrans>& trans, std::vector<std::string>& labels)
{
    std::istringstream lss;
    std::string line;
    state_t src, dst;
    std::string label, quoted_text;
    label_t label_idx;
    prob_t prob;
    std::map<std::string, label_t> label_idx_map;
    unsigned long line_no = 2;

    while (std::getline(fss, line))
    {
        lss = std::istringstream(line);

        // Parse main components
        // ($number, "$text", $number)
        if (lss.ignore(2, '(') &&
            lss >> src &&
            lss.ignore(2, ',') &&
            lss >> std::quoted(quoted_text) &&
            lss.ignore(2, ',') &&
            lss >> dst &&
            lss.ignore(2, ')'))
        {
            // Find label and prob
            size_t split_pos = quoted_text.find("; prob ");
            if (split_pos == std::string::npos)
            {
                std::cerr << "Error: Missing 'prob' in line " << line_no << std::endl;
                return false;
            }

            label = quoted_text.substr(0, split_pos);
            label_idx = label_idx_map.emplace(
                label, label_idx_map.size()
            ).first->second;
            if (label_idx == labels.size())
                labels.push_back(label);

            prob = quoted_text.substr(split_pos + 7);

            trans.emplace_back(src, dst, label_idx, prob);
        }
        else
        {
            std::cerr << "Error: Invalid format in line " << line_no << std::endl;
            return false;
        }
        ++line_no;
    }
    return true;
}

static int handle_error(const std::error_code& error)
{
    const auto& errmsg = error.message();
    std::printf("error mapping file: %s, exiting...\n", errmsg.c_str());
    return error.value();
}

Aut* read_aut_file(std::string& fname)
{
    std::ifstream file(fname);
    if (!file.is_open())
    {
        std::cerr << "Could not open the file " << fname << std::endl;
        return nullptr;
    }
    file.close();

    std::error_code error;
    mio::mmap_source mmap_file = mio::make_mmap_source(fname, error);
    if (error)
    {
        handle_error(error);
        return nullptr;
    }
    if (mmap_file.size() <= 0)
    {
        std::cerr << "File has invalid size" << std::endl;
        return nullptr;
    }

    std::istringstream fss(mmap_file.begin());
    AutDes des;

    if (!parse_des(fss, des)) // TODO: Implement this function
    {
        return nullptr;
    }

    std::cout << "Initial state  : " << des.init_state << std::endl;
    std::cout << "Num transitions: " << des.num_trans << std::endl;
    std::cout << "Num states     : " << des.num_states << std::endl;

    Aut* aut = new Aut(des);

    unsigned long line_no = 2;
    if (!parse_trans(fss, aut->transitions, aut->labels))
    {
        return nullptr;
    }

    mmap_file.unmap();

    return aut;
}
