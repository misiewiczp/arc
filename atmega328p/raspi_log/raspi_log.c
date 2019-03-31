
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <fcntl.h>
#include <cstring>
#include <iostream>
#include <time.h>
#include <unistd.h>

#include "../pwm_read/proto.h"

using namespace std;


/**********************************************************
Declare Global Variables
***********************************************************/

int fd;

spi_command pwm_buf;


/**********************************************************
Declare Functions
***********************************************************/

 unsigned char spiTxRx(unsigned char txDat);



/**********************************************************
Main
  Setup SPI
    Open file spidev0.0 (chip enable 0) for read/write 
      access with the file descriptor "fd"
    Configure transfer speed (1MkHz)
  Start an endless loop that repeatedly sends the characters
    in the hello[] array to the Ardiuno and displays
    the returned bytes
***********************************************************/

int main (void)
{
   fd = open("/dev/spidev0.0", O_RDWR);

   unsigned int speed = 200000;
   unsigned int bits = 8;
   unsigned int mode = 0;
   ioctl (fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
   ioctl (fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
   ioctl (fd, SPI_IOC_WR_MODE, &mode);


   while (1)
   {
      cout << "< ";
      unsigned char c = spiTxRx( REQ_RC );
      cout << (int)c << "\n";
      c = spiTxRx( 0 );
      cout << "RESP: " << (int)c << "\n";
      for(int i = 0; i < SPI_COMMAND_LEN; i++)
      {
        pwm_buf.cval[i] = spiTxRx( 0 );
	usleep(10);
      }

      for (int i = 0; i < SPI_COMMAND_LEN; i++)
        cout << i << "=" << (unsigned int)pwm_buf.cval[i] << "\n";

      cout << "\n";
      cout << "motor: "<<pwm_buf.rc.motor << " "<< pwm_buf.rc.motor_off << " " << (pwm_buf.rc.motor+pwm_buf.rc.motor_off) << "\n";
      cout << "servo: "<<pwm_buf.rc.servo << " "<< pwm_buf.rc.servo_off << " " << (pwm_buf.rc.servo+pwm_buf.rc.servo_off) <<"\n";
      cout << "distance: "<<pwm_buf.rc.distance << "\n";

      usleep(500000);
   }

}

/**********************************************************
spiTxRx
 Transmits one byte via the SPI device, and returns one byte
 as the result.

 Establishes a data structure, spi_ioc_transfer as defined
 by spidev.h and loads the various members to pass the data
 and configuration parameters to the SPI device via IOCTL

 Local variables txDat and rxDat are defined and passed by
 reference.  
***********************************************************/

unsigned char spiTxRx(unsigned char txDat)
{
 
  unsigned char rxDat;

  struct spi_ioc_transfer spi;

  memset (&spi, 0, sizeof (spi));

  spi.tx_buf        = (unsigned long)&txDat;
  spi.rx_buf        = (unsigned long)&rxDat;
  spi.len           = 1;

  ioctl (fd, SPI_IOC_MESSAGE(1), &spi);

  return rxDat;
}