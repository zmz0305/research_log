#include <inttypes.h>
#include <iota/schema/traits/goog_lock_maps.h>
#include "examples/common/devices/smartlock_traits.h"

#include "iota/log.h"
#include "iota/provider/daemon.h"

IotaStatus (*lock_app_on_off_trait_set_state)(GoogOnOff_OnOffState onoff) =
NULL;
IotaStatus (*lock_app_lock_trait_set_state)(GoogLock_LockedState locked_state) =
NULL;

extern GoogSmartLock* g_smartlock;

void lock_on_off_trait_set_state(GoogOnOff* on_off,
                                  GoogOnOff_OnOffState on_off_state) {
    IOTA_LOG_TEST("turning lock %s",
                  (on_off_state == GoogOnOff_ON_OFF_STATE_ON ? "on" : "off"));

    IotaStatus status = (lock_app_on_off_trait_set_state)
                        ? lock_app_on_off_trait_set_state(on_off_state)
                        : kIotaStatusSuccess;
    if (!is_iota_status_success(status)) {
        IOTA_LOG_ERROR("Unable to set switch state.");
        return;
    }
    IOTA_MAP_SET(GoogOnOff_get_state(on_off), state, on_off_state);
}

void lock_lock_trait_set_state(GoogLock* lock, GoogLock_LockedState locked_state) {
    IOTA_LOG_TEST("%s the lock",
                  (locked_state == GoogLock_LOCKED_STATE_LOCKED ? "Lock" : "Unlock"));
    IotaStatus status = (lock_app_lock_trait_set_state)
                        ? lock_app_lock_trait_set_state(locked_state)
                        : kIotaStatusSuccess;
    if(!is_iota_status_success(status)) {
        IOTA_LOG_ERROR("Unable to set lock state.");
        return;
    }
    IOTA_MAP_SET(GoogLock_get_state(lock), locked_state, locked_state);
}


IotaTraitCallbackStatus lock_on_off_trait_setconfig(
        GoogOnOff* self,
        GoogOnOff_SetConfig_Params* params,
        GoogOnOff_SetConfig_Response* response,
        void* user_data) {
    if (!IOTA_MAP_HAS(params, state)) {
        IOTA_LOG_WARN("OnOff SetConfig missing state");
        return kIotaTraitCallbackStatusSuccess;
    }

    lock_on_off_trait_set_state(self, IOTA_MAP_GET(params, state));
    return kIotaTraitCallbackStatusSuccess;
}

IotaTraitCallbackStatus lock_lock_trait_setconfig(
        GoogLock* self,
        GoogLock_SetConfig_Params* params,
        GoogLock_SetConfig_Response* response,
        void* user_data) {
    if(!IOTA_MAP_HAS(params, locked_state)) {
        IOTA_LOG_WARN("Lock trait SetConfig missing state");
        return kIotaTraitCallbackStatusSuccess;
    }

    lock_lock_trait_set_state(self, IOTA_MAP_GET(params, locked_state));
    return kIotaTraitCallbackStatusSuccess;
}


