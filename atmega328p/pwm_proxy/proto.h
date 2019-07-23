
#define SPI_COMMAND_LEN 12

#define REQ_RC 1

typedef struct {
    char req;
    union {
	struct {
	    short distance;
	    short motor;
	    short servo;
	    short motor_applied;
	    short servo_applied;
	    unsigned char idx;
	    unsigned char is_autonomous;
	} rc;
	char cval[SPI_COMMAND_LEN];
    };
} spi_command;
