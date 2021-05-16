#include <stdio.h>

typedef double (*scalar_func)(double);
extern scalar_func capture(double (*)(double, void *), void *);

double monomial(double x, void *n) {
  double y = x;
  for (int i = 1; i < *(int *)n; i++) y *= x;
  return y;
}

int main() {
  int n = 3;
  double x = 2;
  double y = monomial(x, &n);
  printf("%f\n", y);
  double (*cubic)(double) = capture(monomial, (void *)&n);
  y = cubic(x);
  printf("%f\n", y);
  return 0;
}
