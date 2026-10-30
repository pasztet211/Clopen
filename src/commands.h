#ifndef COMMANDS_H
#define COMMANDS_H

#include "interpreter.h"

int execute_command(const Instruction *instruction, Scope *scope);

typedef struct {
    char *value;
    const char *type;
} Operand;

char *trim_copy(const char *start, size_t length);

int resolve_operand(
    const char *text,
    Scope *scope,
    Operand *result
);

int is_numeric_type(const char *type);

#endif