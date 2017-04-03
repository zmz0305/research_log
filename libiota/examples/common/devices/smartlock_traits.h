#ifndef LIBIOTA_EXAMPLES_COMMON_DEVICES_LOCK_TRAITS_H
#define LIBIOTA_EXAMPLES_COMMON_DEVICES_LOCK_TRAITS_H

#ifdef __cplusplus
extern "C" {
#endif

#include "iota/schema/interfaces/goog_smartlock.h"

extern IotaStatus (*lock_app_on_off_trait_set_state)(
        GoogOnOff_OnOffState onoff);

IotaTraitCallbackStatus lock_on_off_trait_setconfig(
        GoogOnOff* self,
        GoogOnOff_SetConfig_Params* params,
        GoogOnOff_SetConfig_Response* response,
        void* user_data);

IotaTraitCallbackStatus lock_lock_trait_setconfig(
        GoogLock* self,
        GoogLock_SetConfig_Params* params,
        GoogLock_SetConfig_Response* response,
        void* user_data);


IotaTraitCallbackStatus lock_temp_units_setting_setconfig(
        GoogTempUnitsSetting* self,
        GoogTempUnitsSetting_SetConfig_Params* params,
        GoogTempUnitsSetting_SetConfig_Response* response,
        void* user_data);

void lock_on_off_trait_set_state(GoogOnOff* on_off,
                                  GoogOnOff_OnOffState on_off_state);

void lock_lock_trait_set_state(GoogLock* lock, GoogLock_LockedState locked_state);

void lock_temp_units_setting_set_state(
        GoogTempUnitsSetting* temp_units_setting,
        GoogTempUnitsSetting_TemperatureUnits temperature_units);

#ifdef __cplusplus
}
#endif


#endif //LIBIOTA_EXAMPLES_COMMON_DEVICES_LOCK_TRAITS_H
