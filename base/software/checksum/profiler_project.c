/*
 * Module:  Profiler_Project.c.
 * Date:    August 10, 2005
 *
 * This example is used to demonstrate the Profiler Tool 'gprof' and compare 
 * the results to those obtained by the Performance Counter and Timestamp 
 * interval timer peripherals to measure code in the 
 * high_res_timestamp_performance_project application.
 * 
 * Details for executing and comparing these applications can be found in 
 * the Profiling Nios II Systems Application Note.
 */

/*
 * Common C Include
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "sys/alt_timestamp.h"
#include "sys/alt_cache.h"
#include "system.h"
#include "nios2.h"
#include "checksum_test.h"

#define HAL_PLATFORM_RESET() NIOS2_WRITE_STATUS(0); NIOS2_WRITE_IENABLE(0); ((void (*) (void)) NIOS2_RESET_ADDR) ()

alt_u32 checksum_start_time, checksum_end_time, i;
alt_u32 checksum_value;
const char* msg = "hello world";




int main()
{


    while(1){

    alt_icache_flush_all();
    alt_dcache_flush_all();

  if (alt_timestamp_start() < 0)
    {
      printf ("No timestamp device is available.\n");
    }


    checksum_start_time = alt_timestamp();
    checksum_value = checksum_test_routine();
    checksum_end_time = alt_timestamp();


    i = checksum_end_time - checksum_start_time;
    printf("%lu\n", i);


    }


//    HAL_PLATFORM_RESET();


}
