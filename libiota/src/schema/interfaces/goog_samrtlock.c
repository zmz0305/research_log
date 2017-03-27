#include "include/iota/schema/interfaces/goog_smartlock.h"

#include "iota/alloc.h"

#include "src/iota_assert.h"
#include "src/schema/interface.h"

struct GoogSmartLock_ {
    IotaInterface base;
    GoogOnOff* power_switch;
    GoogLock* lock;
    // add more features in here
};

/** Base IotaInterface* version of the destroy method. */
void GoogLock_destroy_(IotaInterface* self) {
    GoogSmartLock_destroy((GoogSmartLock *) self);
}

/** Base IotaInterface* version of the get_trait_count method. */
uint16_t GoogLock_get_trait_count_(IotaInterface* self) {
    return GoogSmartLock_get_trait_count((GoogSmartLock *) self);
}

/** Base IotaInterface* version of the get_traits method. */
void GoogLock_get_traits_(IotaInterface* self,
                           IotaTrait** traits,
                           uint16_t expected_trait_count) {
    GoogSmartLock_get_traits((GoogSmartLock *) self, traits, expected_trait_count);
}

/** Base IotaInterface* version of the release_traits method. */
void GoogLock_release_traits_(IotaInterface* self) {
    GoogSmartLock_release_traits((GoogSmartLock *) self);
}

/** IotaInterface vtable for the GoogLock interface. */
static const IotaInterfaceVtable GoogLock_vtable = {
        .destroy = GoogLock_destroy_,
        .get_trait_count = GoogLock_get_trait_count_,
        .get_traits = GoogLock_get_traits_,
        .release_traits = GoogLock_release_traits_,
};

const char kGoogLock_DeviceKindName[] = "Lock";
const IotaDeviceKindCode kGoogLock_DeviceKindCode = {.bytes = "AI"};

GoogSmartLock* GoogSmartLock_create(uint32_t optional_components) {
    GoogSmartLock* self = (GoogSmartLock*)IOTA_ALLOC(sizeof(GoogSmartLock));
    IOTA_ASSERT(self != NULL, "Allocation failure");

    *self = (GoogSmartLock){.base = iota_interface_create(
            &GoogLock_vtable, &kGoogLock_DeviceKindName[0],
            &kGoogLock_DeviceKindCode)};

    self->power_switch = GoogOnOff_create("powerSwitch");

    if (optional_components & GoogLock_WITH_LOCK) {
        self->lock = GoogLock_create("lock");
    }

//    if (optional_components & GoogLock_WITH_ALARM) {
//        self->dimmer = GoogBrightness_create("dimmer");
//    }



    IOTA_LOG_MEMORY_STATS("GoogLock_interface_create");
    return self;
}

void GoogSmartLock_destroy(GoogSmartLock *self) {
    if (self->power_switch) {
        GoogOnOff_destroy(self->power_switch);
    }



    IOTA_FREE(self);
}

uint16_t GoogSmartLock_get_trait_count(GoogSmartLock *self) {
    uint16_t trait_count = 0;

    if (self->power_switch) {
        trait_count++;
    }
    if(self->lock) {
        trait_count++;
    }

    return trait_count;
}

void GoogSmartLock_get_traits(GoogSmartLock *self,
                              IotaTrait **traits,
                              uint16_t expected_trait_count) {
    uint16_t trait_count = 0;
    if (self->power_switch) {
        IOTA_ASSERT(trait_count < expected_trait_count, "Unexpected trait");
        if (trait_count >= expected_trait_count) {
            return;
        }

        traits[trait_count] = (IotaTrait*)self->power_switch;
        trait_count++;
    }

    if(self->lock) {
        IOTA_ASSERT(trait_count < expected_trait_count, "Unexpected trait");
        if(trait_count >= expected_trait_count) {
            return;
        }

        traits[trait_count] = (IotaTrait*)self->lock;
        trait_count++;
    }

}

void GoogSmartLock_release_traits(GoogSmartLock *self) {
    self->power_switch = NULL;
    self->lock = NULL;
}

GoogOnOff* GoogSmartLock_get_power_switch(GoogSmartLock *self) {
    return self->power_switch;
}

GoogLock* GoogSmartLock_get_lock(GoogSmartLock *self) {
    return self->lock;
}
