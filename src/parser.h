#ifndef PARSER_H
#define PARSER_H

#include <stddef.h>
#include "clo_loader.h"

typedef struct Instruction Instruction;
typedef struct InstructionList InstructionList;

typedef struct {
    char *condition;
    InstructionList *block;
    size_t line;
} IfBranch;

struct Instruction {
    char *type;
    size_t line;

    char **parts;
    size_t part_count;

    char *condition;
    IfBranch *branches;
    size_t branch_count;
    InstructionList *else_block;

    char **init;
    size_t init_count;

    char **update;
    size_t update_count;

    char *name;
    char **inputs;
    size_t input_count;

    InstructionList *block;
};

struct InstructionList {
    Instruction *items;
    size_t count;
};

int parse_program(const CloProgram *program, InstructionList *instructions);
void free_instructions(InstructionList *instructions);

#endif
