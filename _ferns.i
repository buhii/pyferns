/*
  Copyright 2012, Takahiro Kamatani
  All rights reserved.

  pyferns is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software
  Foundation; either version 2 of the License, or (at your option) any later
  version.

  pyferns is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE. See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with
  pyferns; if not, write to the Free Software Foundation, Inc., 51 Franklin
  Street, Fifth Floor, Boston, MA 02110-1301, USA
*/

%module pyferns
%include exception.i

%{
  // ------------------------------------------------------------------------------------
  // This code comes from the OpenCV 2.4.0 Python binding: modules/python/src2/cv2.cv.hpp
  // 
  #include <cv.h>
  #include <Python.h>  

  #define OLD_MODULESTR "cv2.cv"

  static int failmsg(const char *fmt, ...)
  {
    char str[1000];

    va_list ap;
    va_start(ap, fmt);
    vsnprintf(str, sizeof(str), fmt, ap);
    va_end(ap);

    PyErr_SetString(PyExc_TypeError, str);
    return 0;
  }

  struct iplimage_t {
    PyObject_HEAD
    IplImage *a;
    PyObject *data;
    size_t offset;
  };

  static PyTypeObject iplimage_Type = {
    PyObject_HEAD_INIT(&PyType_Type)
    0,                                      /*size*/
    OLD_MODULESTR".iplimage",               /*name*/
    sizeof(iplimage_t),                     /*basicsize*/
  };

  static int is_iplimage(PyObject *o)
  {
    return (strcmp(o->ob_type->tp_name,"cv2.cv.iplimage") == 0);
    // return PyType_IsSubtype(o->ob_type, &iplimage_Type);
  }

  static int convert_to_IplImage(PyObject *o, IplImage **dst, const char *name)
  {
    iplimage_t *ipl = (iplimage_t*)o;
    void *buffer;
    Py_ssize_t buffer_len;

    if (!is_iplimage(o)) {
      return failmsg("Argument '%s' must be IplImage", name);
    } else if (PyString_Check(ipl->data)) {
      cvSetData(ipl->a, PyString_AsString(ipl->data) + ipl->offset, ipl->a->widthStep);
      assert(cvGetErrStatus() == 0);
      *dst = ipl->a;
      return 1;
    } else if (ipl->data && PyObject_AsWriteBuffer(ipl->data, &buffer, &buffer_len) == 0) {
      cvSetData(ipl->a, (void*)((char*)buffer + ipl->offset), ipl->a->widthStep);
      assert(cvGetErrStatus() == 0);
      *dst = ipl->a;
      return 1;
    } else {
      return failmsg("IplImage argument '%s' has no data", name);
    }
  }

  // ------------------------------------------------------------------------------------
%}

%typemap(in) IplImage *
{
  if (!convert_to_IplImage($input, &($1), ""))
  {
    SWIG_exception( SWIG_TypeError, "%%typemap: could not convert input argument to an IplImage");
  }
}

%typemap(typecheck) IplImage *
{
  $1 = is_iplimage($input) ? 1 : 0;
}

%typemap(out) int *
{
  $result = PyTuple_New(DETECTOR_TUPLE_LENGTH);
  for (int i = 0; i < DETECTOR_TUPLE_LENGTH; i++) {
    PyObject *o = PyInt_FromSize_t( $1[i] );
    PyTuple_SetItem($result, i, o);
  }
}


%{
  #include "planar_pattern_detector_wrapper.hpp"
%}

%include "planar_pattern_detector_wrapper.hpp"

