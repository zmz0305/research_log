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

// GENERATED FILE, DO NOT EDIT.
// SOURCE: gwv/goog/interfaces/Lock.proto

#ifndef GOOG_LOCK_H_
#define GOOG_LOCK_H_

#include "iota/schema/trait.h"

#include "iota/schema/traits/goog_on_off.h"
#include "iota/schema/traits/goog_lock.h"
#include "iota/schema/traits/goog_temp_units_setting.h"

#ifdef __cplusplus
extern "C" {
#endif

static const uint32_t kGoogSamrtLock_Id = 0x00018006;

typedef struct GoogSmartLock_ GoogSmartLock;

// Definitions for optional components.
#define GoogLock_WITHOUT_OPTIONAL_COMPONENTS 0
#define GoogLock_WITH_LOCK (1 << 0)
#define GoogLock_WITH_ALARM (1 << 1)
#define GoogLock_WITH_TEMPUNITSETTING (1 << 2)
#define GoogLock_WITH_ALL_COMPONENTS (~0)

/**
 * Create a new GoogLock interface.
 *
 * Optional components can be enabled by or'ing together the defines above and
 * passing the result as the optional_components parameter.
 */
GoogSmartLock* GoogSmartLock_create(uint32_t optional_components);

/**
 * Free the memory used by this interface object.
 *
 * If the component traits are still owned by the interface, they will be
 * destroyed as well.
 */
void GoogSmartLock_destroy(GoogSmartLock *self);

/**
 * Returns the number of traits enabled on this interface.
 */
uint16_t GoogSmartLock_get_trait_count(GoogSmartLock *self);

/**
 * Copy this interface's component traits into the given IotaTrait array.
 *
 * Callers must allocate the array before calling this function.  Use
 * iota_interface_get_trait_count to determine an appropriate size.
 */
void GoogSmartLock_get_traits(GoogSmartLock *self,
                              IotaTrait **traits,
                              uint16_t expected_trait_count);

/**
 * Releases ownership of the component traits, so that they are not freed by
 * GoogLock_destroy.
 *
 * Call this function after calling create_trait_array in order to become the
 * owner of the component traits.  After this call, the interface will NULL out
 * its pointers to the component traits.  It'll be useless except for the fact
 * that the caller still needs to invoke GoogLock_destroy to free
 * the interface object itself.
 */
void GoogSmartLock_release_traits(GoogSmartLock *self);

/**
 * Returns a pointer to the power_switch component from this interface.
 *
 * May return NULL if the traits have been released.
 */
GoogOnOff* GoogSmartLock_get_power_switch(GoogSmartLock *self);

GoogLock* GoogSmartLock_get_lock(GoogSmartLock *self);

GoogTempUnitsSetting* GoogSmartLock_get_temp_units_setting(GoogSmartLock *self);
#ifdef __cplusplus
}
#endif

#endif  // GOOG_LOCK_H_
