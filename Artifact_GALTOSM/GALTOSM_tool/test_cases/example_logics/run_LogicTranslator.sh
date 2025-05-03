#!/bin/bash

# Get the absolute path to the directory this script is in
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the Python file relative to BASE_DIR
PYTHON_FILE="$BASE_DIR/../../source_code/logic_translator_tool/logic_translator.py"


APCTL="APCTL"
APCTLS="APCTLS"
APRCTL="APRCTL"
PCTL="PCTL"
PCTLS="PCTLS"
PRCTL="PRCTL"


TYPE=$APCTL

echo APCTL
LOGIC="(P=?[(true)_(true)U_(\"LIVE\")(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P=?[(true)_(true)U_(\"LAST_GOT_SEAT\")(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P=?[X_tau((true)&(true))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P>0.4[X_((\"act1\" | \"act2\"))(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P=?[(true)_(true)U_(\"HOME\" | \"DRUNK\")(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P=?[(true)_(\"ATTEMPT\" | \"SUCCESS_FRAME\" | \"ACK_FAIL\" | \"RETRY1\" | \"RETRY2\")U_(\"SUCCESS_FILE\")(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 



TYPE=$APCTLS

echo APCTLS
LOGIC="(P=?[((X(true))&(X_(\"act1\" | \"act2\")(true)))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P<=0.65[((true)U(!(X(true))))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P<=0.65[((X_(\"a\" | \!\"b\")(true))U(!(X(true))))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 



TYPE=$APRCTL
echo APRCTL
LOGIC="(E=?[(P>=1[X_(\"ONE\" | \"TWO\" | \"THREE\" | \"FOUR\" | \"FIVE\" | \"SIX\")(true)])])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(E=?[(!((!(P>=1[X_(\"LIVE\")(true)]))&(!(P>=1[X_(\"DEAD\")(true)]))))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(E=?[(!((!(P>=1[X_(\"HOME\")(true)]))&(!(P>=1[X_(\"DRUNK\")(true)]))))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 



TYPE=$PCTL

echo PCTL
LOGIC="(\!(\"ap\"))"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P<0.24[(true)U(\"ap1\")])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="(P<0.24[(P<0.2[X(\"ap1\")])U(\"ap2\")])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 
LOGIC="((P<0.24[(true)U(\"ap1\")])|(P<0.24[(P<0.2[X(\"ap1\")])U(\"ap2\")]))"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 


TYPE=$PCTLS

echo PCTLS
LOGIC="(P<0.24[(X(false))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo
LOGIC="(P>=0.14[((\"ap1\")U(\"ap2\"))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo
LOGIC="(P=?[((x("ap1"))&(("ap2")U("ap3")))])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo
LOGIC="([P>=0.3[((true)U((!(\"rep\"))&(!(\"recv\"))))]])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo 

TYPE=$PRCTL

echo PRCTL
LOGIC="(R=?[(true)])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"
echo
LOGIC="(R=?[(P>0.0[(true)U(\"ap\")])])"
python3 "$PYTHON_FILE" "$TYPE" "$LOGIC"

