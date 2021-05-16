GCCFLAGS = -Wall -Wextra -g

better_lambda: better_lambda.o better_lambda.c
	gcc -o better_lambda $(GCCFLAGS) better_lambda.c better_lambda.o

better_lambda.o: better_lambda.f90
	gfortran -fPIC $(GCCFLAGS) -c better_lambda.f90
