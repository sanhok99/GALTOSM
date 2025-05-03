#ifndef AUT_HPP
#define AUT_HPP 1

#include <map>
#include <string>
#include <vector>

typedef unsigned long state_t;
typedef unsigned short label_t;
typedef std::string prob_t;

/// @brief Struct for the automaton description
/// @details The description contains the initial state,
/// the number of transitions and the number of states.
struct AutDes
{
    state_t init_state;
    state_t num_trans;
    state_t num_states;
};

/// @brief Struct for the automaton transition
/// @details The transition contains the source state,
/// the destination state, the label index and the probability.
struct AutTrans
{
    state_t src;
    state_t dst;
    label_t lbl_idx;
    prob_t prob;

    AutTrans(state_t src, state_t dst, label_t lbl_idx, prob_t prob);
};

/// @brief Automaton class to store the .aut file graph information
class Aut
{
friend Aut* read_aut_file(std::string& fname);

private:
    std::vector<std::string> labels;
    std::vector<AutTrans> transitions;

public:
    const AutDes des;

    /// @brief Constructor for the automaton
    /// @param des The description of the automaton
    Aut(AutDes des);

    /// @brief Get the labels of the automaton
    /// @return the vector of labels
    const std::vector<std::string>& get_labels() const;

    /// @brief Get the transitions of the automaton
    /// @return the vector of transitions
    const std::vector<AutTrans>& get_transitions() const;
};


/// @brief Read the `.aut` file and construct an object
/// @param fname The path to the file
/// @return the pointer to `Aut` object
Aut* read_aut_file(std::string& fname);

/// @brief Convert the aut to lab and tra files
/// @param aut
/// @param lab_fname Save path for the label file
/// @param tra_fname Save path for the transition file
/// @param storm If true, write output in storm style, else in prism style.
bool aut_convert(Aut* aut, std::string lab_fname, std::string tra_fname, bool storm);


#endif // AUT_HPP