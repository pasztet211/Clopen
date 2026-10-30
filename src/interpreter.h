#ifndef INTERPRETER_H
#define INTERPRETER_H

#include "parser.h"

typedef struct {
    char *name;
    char *value;
    char *type;
    int read_only;
} Variable;

typedef struct Scope Scope;

typedef struct {
    const Instruction *instruction;
    Scope *closure;
} Function;

typedef struct {
    Function *items;
    size_t count;
} FunctionList;

enum {
    EXEC_OK = 0,
    EXEC_ERROR = 1,
    EXEC_SHALT = 2,
    EXEC_HALT = 3
};

typedef struct {
    Variable *items;
    size_t count;
} VariableList;

struct Scope {
    VariableList variables;
    Scope *parent;
    size_t ref_count;
};

typedef struct {
    Scope *scope;
    FunctionList functions;
    int in_function;
    int returned;
    char *return_value;
    char *return_type;
} ExecutionContext;

int execute_instructions(
    const InstructionList *instructions,
    ExecutionContext *context
);

void free_variables(VariableList *variables);

#endif