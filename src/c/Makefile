
CC 			:= gcc
CFLAGS 		:= -c -fPIC -Wsign-conversion -Wsign-compare
SOURCES 	:= $(wildcard *.c)
OUTPUTS 	:= $(SOURCES:.c=.o)

all: $(OUTPUTS)

%.o: %.c *.h
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean
clean:
	@ rm -f *.o

