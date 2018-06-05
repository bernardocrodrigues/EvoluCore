
#include <stdio.h>
#include "sys/alt_timestamp.h"
#include "sys/alt_cache.h"
#include "system.h"
#include "nios2.h"


#define HAL_PLATFORM_RESET() NIOS2_WRITE_STATUS(0); NIOS2_WRITE_IENABLE(0); ((void (*) (void)) NIOS2_RESET_ADDR) ()


int main()
{

  if (alt_timestamp_start() < 0)
    {
      printf ("No timestamp device is available.\n");
    }

alt_icache_flush_all();
alt_dcache_flush_all();

alt_u32 checksum_start_time = alt_timestamp();

printf("Hello A\n");
printf("Hello A\n");
printf("Hello A\n");


alt_u32 checksum_end_time = alt_timestamp();

alt_u32 i = checksum_end_time - checksum_start_time;
printf("%ld\n", i);


HAL_PLATFORM_RESET();


}
