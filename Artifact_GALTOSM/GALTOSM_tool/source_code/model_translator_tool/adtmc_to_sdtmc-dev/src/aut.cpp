#include "aut.hpp"

AutTrans::AutTrans(state_t src, state_t dst, label_t lbl_idx, prob_t prob)
: src(src), dst(dst), lbl_idx(lbl_idx), prob(prob)
{}

Aut::Aut(AutDes des)
: des(des)
{
    this->transitions.reserve(des.num_trans);
}

const std::vector<std::string>& Aut::get_labels() const
{
    return labels;
}

const std::vector<AutTrans>& Aut::get_transitions() const
{
    return transitions;
}