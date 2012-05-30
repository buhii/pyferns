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
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

#include "planar_pattern_detector_wrapper.hpp"
#include "planar_pattern_detector_builder.h"


planar_pattern_detector_wrapper::planar_pattern_detector_wrapper(void)
{
  affine_transformation_range range;
}

planar_pattern_detector_wrapper::~planar_pattern_detector_wrapper(void)
{
  delete detector;
}

bool planar_pattern_detector_wrapper::just_load(const char * detector_data_filename)
{
  detector = planar_pattern_detector_builder::just_load(detector_data_filename);
  return !(!detector);
}

bool planar_pattern_detector_wrapper::save(const char * detector_data_filename)
{
  return false;
}

bool planar_pattern_detector_wrapper::learn(const CvMat* input_image)
{
  // zlib strings
  return false;
}

bool planar_pattern_detector_wrapper::detect(const CvMat* input_image)
{
  return false;
}
