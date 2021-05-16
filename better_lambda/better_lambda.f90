module better_lambda
  use iso_c_binding, only: c_double, c_ptr, c_funloc, c_funptr, c_f_procpointer

  implicit none

  public capture

  interface
     function c_func(x, params) bind(c) result(y)
       import c_double, c_funptr, c_ptr
       real(c_double), value :: x
       type(c_ptr), value :: params
       real(c_double) :: y
     end function c_func
  end interface
contains
  function capture(f_ptr, params) bind(c) result(closure)
    type(c_funptr), value :: f_ptr
    type(c_ptr), value :: params
    type(c_funptr) :: closure
    procedure(c_func), pointer :: f

    call c_f_procpointer(f_ptr, f)
    closure = c_funloc(fortran_closure)
  contains
    function fortran_closure(x) result(y)
      real(c_double), value :: x
      real(c_double) :: y

      y = f(x, params)
    end function fortran_closure
  end function capture
end module better_lambda
