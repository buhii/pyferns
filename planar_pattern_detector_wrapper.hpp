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
#include <cv.h>

#ifndef PLANAR_PATTERN_DETECTOR_WRAPPER_HPP
#define PLANAR_PATTERN_DETECTOR_WRAPPER_HPP

#define DETECTOR_TUPLE_LENGTH 8

using namespace std;

#include "planar_pattern_detector.h"

// --------------------------------------------------------------------------
// Thin wrapper to learn and detect
// --------------------------------------------------------------------------
class planar_pattern_detector_wrapper
{
 public:
  planar_pattern_detector_wrapper(void);

  ~planar_pattern_detector_wrapper(void);

  bool just_load(const char * detector_data_filename);
  bool save(const char * detector_data_filename);

  bool learn(const char * image_name);
  int * detect(const IplImage* input_image);

  planar_pattern_detector * detector;
  int result[8];
};

#endif // PLANAR_PATTERN_DETECTOR_WRAPPER_HPP
