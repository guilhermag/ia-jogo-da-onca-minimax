CFLAGS = -g -Wall -Wno-unused-result -O3
LDLIBS = -l hiredis -l readline

all: controlador

controlador: controlador.c tabuleiro.c tabuleiro.h
	$(CC) $(CFLAGS) controlador.c tabuleiro.c -o $@ $(LDLIBS)
clean:
	rm -f controlador exemplo1 exemplo2
