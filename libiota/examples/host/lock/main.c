#include "examples/common/devices/smartlock.h"
#include "examples/host/framework/dev_framework.h"

#include "iota/log.h"
#include "iota/version.h"

IotaDaemon* g_iota_daemon = NULL;
GoogSmartLock* g_smartlock = NULL;

static host_cli_command host_cli_lock_commands[] = {
        {.name = "iota-update-power-switch",
                .help = "Turn on/off power switch",
                .function = example_lock_update_power_switch_cli},
};

static IotaDaemon* create_lock_daemon_(void) {
    IOTA_LOG_INFO("Inside create_lock_daemon_");

    // Create the example lock interface.
    g_smartlock = GoogSmartLock_create(GoogLock_WITH_ALL_COMPONENTS);

    IotaDevice* iota_device = iota_device_create_from_interface(
            (IotaInterface*)g_smartlock,
            (IotaDeviceInfo){
                    .model_manifest_id = "AIAAA",
//                    .model_manifest_id = "LOCKA",
                    .firmware_version = "My Lock, libiota " IOTA_VERSION_STRING,
                    .serial_number = "1.0.0",
                    .interface_version = "0"});
    if (iota_device == NULL) {
        IOTA_LOG_ERROR("Device create from interface failed");
        GoogSmartLock_destroy(g_smartlock);
        return NULL;
    }

    g_iota_daemon = host_framework_create_daemon("lock", iota_device);

    // Set default state of traits on the lock.
    example_lock_configure(g_smartlock, g_iota_daemon);

    return g_iota_daemon;
}

int main(int argc, char** argv) {
    HostIotaFrameworkConfig config = (HostIotaFrameworkConfig){
            .base =
            (IotaFrameworkConfig){
                    .cli_commands = host_cli_lock_commands,
                    .num_commands = COUNT_OF(host_cli_lock_commands),
                    .builder = create_lock_daemon_,
            },
            .argc = argc,
            .argv = argv,
            .user_data = NULL,
            .name = "lock",
    };
    return host_framework_main(&config);
}
