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
%{
  #include "planar_pattern_detector_wrapper.hpp"
%}

%include "planar_pattern_detector_wrapper.hpp"

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

  struct cvmat_t {
    PyObject_HEAD
    CvMat *a;
    PyObject *data;
    size_t offset;
  };

  static PyTypeObject cvmat_Type = {
    PyObject_HEAD_INIT(&PyType_Type)
    0,                                      /*size*/
    OLD_MODULESTR".cvmat",                  /*name*/
    sizeof(cvmat_t),                        /*basicsize*/
  };

  static int is_cvmat(PyObject *o)
  {
    return PyType_IsSubtype(o->ob_type, &cvmat_Type);
  }

  static int convert_to_CvMat(PyObject *o, CvMat **dst, const char *name)
  {
    cvmat_t *m = (cvmat_t*)o;
    void *buffer;
    Py_ssize_t buffer_len;

    if (!is_cvmat(o)) {
      //#if !PYTHON_USE_NUMPY
      return failmsg("Argument '%s' must be CvMat. Use fromarray() to convert numpy arrays to CvMat", name);
      /*#else
	PyObject *asmat = fromarray(o, 0);
	if (asmat == NULL)
	return failmsg("Argument '%s' must be CvMat", name);
	// now have the array obect as a cvmat, can use regular conversion
	return convert_to_CvMat(asmat, dst, name);
	#endif*/
    } else {
      m->a->refcount = NULL;
      if (m->data && PyString_Check(m->data)) {
	assert(cvGetErrStatus() == 0);
	char *ptr = PyString_AsString(m->data) + m->offset;
	cvSetData(m->a, ptr, m->a->step);
	assert(cvGetErrStatus() == 0);
	*dst = m->a;
	return 1;
      } else if (m->data && PyObject_AsWriteBuffer(m->data, &buffer, &buffer_len) == 0) {
	cvSetData(m->a, (void*)((char*)buffer + m->offset), m->a->step);
	assert(cvGetErrStatus() == 0);
	*dst = m->a;
	return 1;
      } else if (m->data && m->a->data.ptr){
	*dst = m->a;  
	return 1;   
      }
      else {
	return failmsg("CvMat argument '%s' has no data", name);
      }
    }
  }

  // ------------------------------------------------------------------------------------
%}

%typemap(in) CvMat *
{
  if (!convert_to_CvMat($input, &($1), ""))
  {
    SWIG_exception( SWIG_TypeError, "%%typemap: could not convert input argument to an CvMat");
  }
}

%typemap(typecheck) CvMat *
{
  $1 = is_cvmat($input) ? 1 : 0;
}

%typemap(out) int *
{
  int i;
  $result = PyTuple_New(DETECTOR_TUPLE_LENGTH);
  for (int i = 0; i < DETECTOR_TUPLE_LENGTH; i++) {
    PyObject *o = PyInt_FromSize_t( $1[i] );
    PyTuple_SetItem($result, i, o);
  }
}
