#ifndef CLO_LOADER_H
#define CLO_LOADER_H

#include <stddef.h>

typedef struct {
    char *text;
    size_t line_number;
} CloLine;

typedef struct {
    CloLine *lines;
    size_t count;
} CloProgram;

int load_clo(const char *filename, CloProgram *program);
void free_clo(CloProgram *program);

#endif