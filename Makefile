CC = python3
EXEC = flycombi.py
ARGV1 = aeropuertos.csv
ARGV2 = vuelos.csv

run:
	$(CC) $(EXEC) $(ARGV1) $(ARGV2) < comandos.txt