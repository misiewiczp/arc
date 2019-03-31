
#define SPI_COMMAND_LEN 11

#define REQ_RC 1

typedef struct {
    char req;
    union {
	struct {
	    short distance;
	    short motor;
	    short servo;
	    short motor_off;
	    short servo_off;
	    unsigned char idx;
	} rc;
	char cval[SPI_COMMAND_LEN];
    };
} spi_command;
