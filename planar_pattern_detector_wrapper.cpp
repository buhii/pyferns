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
  detector = new planar_pattern_detector();
}

planar_pattern_detector_wrapper::~planar_pattern_detector_wrapper(void)
{
  delete detector;
}

bool planar_pattern_detector_wrapper::just_load(const char * detector_data_filename)
{
  delete detector;
  detector = planar_pattern_detector_builder::just_load(detector_data_filename);
  detector->set_maximum_number_of_points_to_detect(1000);
  return !(!detector);
}

bool planar_pattern_detector_wrapper::save(const char * detector_data_filename)
{
  return detector->save(detector_data_filename);
}

bool planar_pattern_detector_wrapper::learn(const char * image_name)
{
  delete detector;
  affine_transformation_range range;
  detector = planar_pattern_detector_builder::learn(image_name,
						    &range,
						    400,
						    5000,
						    0.0,
						    32, 7, 4,
						    30, 12,
						    10000, 200);
  return !(!detector);
}

int * planar_pattern_detector_wrapper::detect(const IplImage * input_image)
{
  int result[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  detector->detect(input_image);

  if (detector->pattern_is_detected) {
    result[0] = detector->detected_u_corner[0];
    result[1] = detector->detected_v_corner[0];
    result[2] = detector->detected_u_corner[1];
    result[3] = detector->detected_v_corner[1];
    result[4] = detector->detected_u_corner[2];
    result[5] = detector->detected_v_corner[2];
    result[6] = detector->detected_u_corner[3];
    result[7] = detector->detected_v_corner[3];
  }
  return result;
}

