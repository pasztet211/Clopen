#ifndef HELPER_COMMANDS_H
#define HELPER_COMMANDS_H

#include "interpreter.h"

Variable *find_variable(Scope *scope, const char *name);
char *copy_string(const char *string);
char *parse_value(const char *value, const char *type);

int create_variable(Scope *scope, const char *name,
                    const char *value, const char *type);

int change_variable(Scope *scope, const char *name,
                    const char *value, const char *type);

int delete_variable(Scope *scope, const char *name);
void free_scope(Scope *scope);
void retain_scope(Scope *scope);
void release_scope(Scope *scope);
Scope *create_scope(Scope *parent);
#endif