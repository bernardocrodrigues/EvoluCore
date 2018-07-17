 

#include "sys/alt_timestamp.h"
#include "sys/alt_cache.h"
#include "system.h"
#include "nios2.h"


#define HAL_PLATFORM_RESET() NIOS2_WRITE_STATUS(0); NIOS2_WRITE_IENABLE(0); ((void (*) (void)) NIOS2_RESET_ADDR) ()

#include <stdio.h>


#define NDIGITS 100          //max digits to compute
#define LEN (NDIGITS/4+1)*14   //nec. array length

long a[LEN];                   //array of 4-digit-decimals
long b;                        //nominator prev. base
long c = LEN;                  //index
long d;                        //accumulator and carry
long e = 0;                    //save previous 4 digits
long f = 10000;                //new base, 4 decimal digits
long g;                        //denom previous base
long h = 0;                    //init switch

int main(void) {
        for(; (b=c-=14) > 0 ;){    //outer loop: 4 digits per loop
                for(; --b > 0 ;){      //inner loop: radix conv
                        d *= b;            //acc *= nom prev base
                        if( h == 0 )
                                d += 2000*f;   //first outer loop
                        else
                                d += a[b]*f;   //non-first outer loop
                        g=b+b-1;           //denom prev base
                        a[b] = d % g;
                        d /= g;            //save carry
                }
                h = printf("%d",e+d/f);//print prev 4 digits
                //h = 1;
                d = e = d % f;         //save currently 4 digits
                                       //assure a small enough d
        }
        return 0;

}
