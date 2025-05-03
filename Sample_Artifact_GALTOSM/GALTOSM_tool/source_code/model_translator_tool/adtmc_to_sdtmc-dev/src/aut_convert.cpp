#include "aut.hpp"

#include <fstream>
#include <iostream>
#include <iomanip>

typedef std::map<std::pair<state_t, label_t>, state_t> pair_map_t;

static void generate_states_map(Aut* aut, pair_map_t& gen_states)
{
    std::pair<state_t, label_t> labeled_state;
    auto transitions = aut->get_transitions();

    for (AutTrans trans : transitions)
    {
        labeled_state = std::make_pair(trans.dst, trans.lbl_idx);
        gen_states.emplace(std::move(labeled_state), 0);
    }

    state_t gen_state_id = aut->des.num_states;

    for (auto& [key, val] : gen_states)
    {
        val = gen_state_id++;
    }
}

static bool aut_to_lab_storm(Aut* aut, std::string& fname, const pair_map_t& added_states)
{
    std::ofstream file(fname);

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open file \"" << fname << "\"" << std::endl;
        return false;
    }

    std::vector<std::string> labels = aut->get_labels();
    std::pair<state_t, label_t> state_label;

    file << "#DECLARATION\n";
    file << "init bot";
    for (std::string label : labels)
    {
        file << " " << label;
    }
    file << std::endl;

    file << "#END\n";

    // Add the states that were already there in the Aut
    state_t state;
    for (state = 0; state < aut->des.num_states; state++)
    {
        file << state;
        if (__builtin_expect(state == aut->des.init_state, 0))
        {
            file << " init";
        }
        file << " bot\n";
    }
    // Add the generated states and their labels
    for (auto const& [key, val] : added_states)
    {
        file << val;
        file << ' ' << labels[key.second];
        file << "\n";
    }
    std::cout << "Saved to " << fname << '\n';
    file.close();

    return true;
}

static bool aut_to_lab_prism(Aut* aut, std::string& fname, const pair_map_t& added_states)
{
    std::ofstream file(fname);

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open file \"" << fname << "\"" << std::endl;
        return false;
    }

    std::vector<std::string> labels = aut->get_labels();
    std::pair<state_t, label_t> state_label;

    file << "0=\"init\" 1=\"bot\"";
    label_t i = 2;
    for (std::string label : labels)
    {
        file << " " << i << "=\"" << label << '"';
        i++;
    }
    file << '\n';


    // Add the states that were already there in the Aut
    state_t state;
    for (state = 0; state < aut->des.num_states; state++)
    {
        file << state << ':';
        if (__builtin_expect(state == aut->des.init_state, 0))
        {
            file << " 0";
        }
        file << " 1\n";
    }
    // Add the generated states and their labels
    for (auto const& [key, val] : added_states)
    {
        file << val << ':';
        file << ' ' << key.second+2;
        file << "\n";
    }
    std::cout << "Saved to " << fname << '\n';
    file.close();

    return true;
}

static bool aut_to_tra_storm(Aut* aut, std::string& fname, const pair_map_t& added_states)
{
    std::ofstream file(fname);

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open file \"" << fname << "\"" << std::endl;
        return false;
    }

    file << "dtmc\n";
    file << std::fixed << std::setprecision(6);

    state_t state;
    auto transitions = aut->get_transitions();

    for (AutTrans trans : transitions)
    {
        state = added_states.at({trans.dst, trans.lbl_idx});
        file << trans.src << " ";
        file << state << " ";
        file << trans.prob;
        file << "\n";
    }
    // iterate over each key value of the map added_states:
    for (auto const& [key, val] : added_states)
    {
        file << val << " ";
        file << key.first << " 1";
        file << "\n";
    }
    std::cout << "Saved to " << fname << '\n';
    file.close();

    return true;
}

static bool aut_to_tra_prism(Aut* aut, std::string& fname, const pair_map_t& added_states)
{
    std::ofstream file(fname);

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open file \"" << fname << "\"" << std::endl;
        return false;
    }

    file << std::fixed << std::setprecision(6);
    file << aut->des.num_states + added_states.size() << ' ' << aut->des.num_trans + added_states.size() << '\n';

    state_t state;
    auto transitions = aut->get_transitions();

    for (AutTrans trans : transitions)
    {
        state = added_states.at({trans.dst, trans.lbl_idx});
        file << trans.src << " ";
        file << state << " ";
        file << trans.prob << "\n";
    }
    // iterate over each key value of the map added_states:
    for (auto const& [key, val] : added_states)
    {
        file << val << " ";
        file << key.first << " 1";
        file << "\n";
    }
    std::cout << "Saved to " << fname << '\n';
    file.close();

    return true;
}

bool aut_convert(Aut* aut, std::string lab_fname, std::string tra_fname, bool storm)
{
    pair_map_t gen_states;
    generate_states_map(aut, gen_states);

    std::ios::sync_with_stdio(false);

    if (storm)
    {
        if (!aut_to_lab_storm(aut, lab_fname, gen_states))
            return false;
        if (!aut_to_tra_storm(aut, tra_fname, gen_states))
            return false;
    }
    else
    {
        if (!aut_to_lab_prism(aut, lab_fname, gen_states))
            return false;
        if (!aut_to_tra_prism(aut, tra_fname, gen_states))
            return false;
    }

    return true;
}