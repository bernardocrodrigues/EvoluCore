


#define _GNU_C_SOURCE
#include <stdio.h>
#include <math.h>
#include <complex.h>
#define D(z1,z2) cabs((z1)-(z2))
#define MIN(a,b) ((a<b)?(a):(b))

#define SIZE 4
#define SIZEP 4.0

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

    char area[SIZE*2][SIZE*2][3];
    /* Roots of z^3-1 = 0 */
    complex double z,
        r1 = 1 + 0*I,
        r2 = -0.5 + sin(2*M_PI/3.0)*I,
        r3 = -0.5 - sin(2*M_PI/3.0)*I;



    /* Go from -1 to +1 along real and imag axes */
    for ( int im=-SIZE; im<SIZE; im++ )



        for ( int re=-SIZE, iter; re<SIZE; iter=0, re++ )
        {


            /* Translate the coordinates */
            z = (re/SIZEP) + (im/SIZEP)*I;
            /* Count number of Newton iterations to solve */
            while ( MIN(D(z,r1),MIN(D(z,r2),D(z,r3)))>1e-6 &&
                    iter++<32
            ) z = z - (z*z*z-1.0) / (z*z*3.0);
            /* Color-code the point by distance to roots */
            area[im+SIZE][re+SIZE][0] = iter * D(z,r1);
            area[im+SIZE][re+SIZE][1] = iter * D(z,r2);
            area[im+SIZE][re+SIZE][2] = iter * D(z,r3);
        }
    /* Write the map as a PPM image file */



alt_u32 checksum_end_time = alt_timestamp();

alt_u32 i = checksum_end_time - checksum_start_time;
printf("%ld\n", i);


HAL_PLATFORM_RESET();

}