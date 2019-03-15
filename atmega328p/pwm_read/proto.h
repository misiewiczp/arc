
#define SPI_COMMAND_LEN 8

#define REQ_RC 1

typedef struct {
    char req;
    union {
	struct {
	    short motor;
	    short servo;
	    short motor_off;
	    short servo_off;
	} rc;
	char cval[SPI_COMMAND_LEN];
    };
} spi_command;
