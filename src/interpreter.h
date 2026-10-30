#ifndef INTERPRETER_H
#define INTERPRETER_H

#include "parser.h"

typedef struct {
    char *name;
    char *value;
    char *type;
} Variable;

typedef struct {
    Variable *items;
    size_t count;
} VariableList;

int execute_instructions(
    const InstructionList *instructions,
    VariableList *variables
);

void free_variables(VariableList *variables);

#endif