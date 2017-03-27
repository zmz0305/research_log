#include "examples/common/devices/smartlock.h"
#include "examples/common/devices/smartlock_traits.h"
#include "examples/common/utils.h"

#include "iota/log.h"
#include "iota/provider/daemon.h"
#include "iota/status.h"
#include "iota/version.h"

extern IotaDaemon* g_iota_daemon;
extern GoogSmartLock* g_smartlock;

/**
 * Set default values for the traits and call the set_state method to let the
 * application callback take action based on it. Doing this would ensure that
 * traits are set with default values even when application callback method
 * fails.
 */
void example_lock_configure(GoogSmartLock* lock, IotaDaemon* daemon) {
    // Set default power switch configuration.
    GoogOnOff* onoff_trait = GoogSmartLock_get_power_switch(lock);
    GoogOnOff_set_callbacks(
            onoff_trait, daemon,
            (GoogOnOff_Handlers){.set_config = &lock_on_off_trait_setconfig});
    lock_on_off_trait_set_state(onoff_trait, GoogOnOff_ON_OFF_STATE_ON);
    IOTA_MAP_SET_DEFAULT(GoogOnOff_get_state(onoff_trait), state,
                         GoogOnOff_ON_OFF_STATE_ON);

    // Set default lock config if it exists
    GoogLock* lock_trait = GoogSmartLock_get_lock(lock);
    GoogLock_set_callbacks(
            lock_trait, daemon,
            (GoogLock_Handlers){.set_config = &lock_lock_trait_setconfig});
    lock_lock_trait_set_state(lock_trait, GoogLock_LOCKED_STATE_LOCKED);
    IOTA_MAP_SET_DEFAULT(GoogLock_get_state(lock_trait), locked_state,
                         GoogLock_LOCKED_STATE_LOCKED);

}

static void example_set_power_switch_callback_(void* context) {
    GoogOnOff* power_switch = GoogSmartLock_get_power_switch(g_smartlock);
    lock_on_off_trait_set_state(power_switch, (GoogOnOff_OnOffState)context);
}

int32_t example_lock_update_power_switch_with_status(int32_t argc,
                                                      char** argv) {
    if (!g_iota_daemon) {
        IOTA_LOG_ERROR("Daemon not initialized");
        return -1;
    }

    if (!g_smartlock) {
        IOTA_LOG_ERROR("Lock not initialized");
        return -1;
    }

    if (argc != 2) {
        IOTA_LOG_INFO("Expected on / off state");
        return -1;
    }

    GoogOnOff_OnOffState onoff_state;
    if (!strcasecmp(argv[1], "on")) {
        onoff_state = GoogOnOff_ON_OFF_STATE_ON;
    } else if (!strcasecmp(argv[1], "off")) {
        onoff_state = GoogOnOff_ON_OFF_STATE_OFF;
    } else {
        IOTA_LOG_INFO("Invalid power switch state");
        return -1;
    }

    if (iota_daemon_queue_application_job) {
        iota_daemon_queue_application_job(
                g_iota_daemon, example_set_power_switch_callback_, (void*)onoff_state);
    }

    return 0;
}

void example_lock_update_power_switch_cli(int argc, char** argv) {
    example_lock_update_power_switch_with_status(argc, argv);
}
