//
// Created by zmz on 23/03/17.
//
/*
 * Copyright 2017 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef LIBIOTA_EXAMPLES_COMMON_DEVICES_LIGHT_H_
#define LIBIOTA_EXAMPLES_COMMON_DEVICES_LIGHT_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "iota/daemon.h"
#include "iota/schema/interfaces/goog_smartlock.h"
#include <inttypes.h>

/**
 * Sets the default state of every trait.
 */
void example_lock_configure(GoogSmartLock* lock, IotaDaemon* daemon);

int32_t example_lock_update_power_switch_with_status(int32_t argc,
                                                      char** argv);

void example_lock_update_power_switch_cli(int argc, char** argv);
#ifdef __cplusplus
}
#endif

#endif  // LIBIOTA_EXAMPLES_COMMON_DEVICES_LIGHT_H_

