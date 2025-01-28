#include "ZIRE_HAL.h"
#include <thread> 
#include <chrono>
/* Assume that any non-Windows platform uses POSIX-style sockets instead. */
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>  /* Needed for getaddrinfo() and freeaddrinfo() */
#include <unistd.h> /* Needed for close() */


int sockCTRL, sockSTREAM;
int ret;
int ctrl_port = 9000, stream_port = 8000;
fd_set set;
struct timeval timeout;

ZIRE_HAL::ZIRE_HAL() {
	connected_ctrl = false;
	connected_stream = false;
};

ZIRE_HAL::~ZIRE_HAL() {
};

NI_RESULT ZIRE_HAL::sockInit(void)
{
	return NI_OK;
}

NI_RESULT ZIRE_HAL::sockQuit(void)
{
	return NI_OK;
}
    
NI_RESULT ZIRE_HAL::Connect(string path, bool istesting) {
	if (connected_ctrl) {
		return NI_ALREADY_CONNECTED;
	}
	else {
		sockaddr_in clientCTRL;
		clientCTRL.sin_family = AF_INET;
		clientCTRL.sin_addr.s_addr = inet_addr(path.c_str());
		clientCTRL.sin_port = htons(ctrl_port);

		sockCTRL = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (sockCTRL == -1) {
			perror("Socket creation error");
			return NI_ERROR_SOCKET;
		}

		if (connect(sockCTRL, (struct sockaddr*) &clientCTRL, sizeof(clientCTRL)) == -1) {
			perror("Connection error");
			close(sockCTRL);
			return NI_ERROR_SOCKET;
		}
    
		connected_ctrl = true;
		ConnectSTREAM(path);
		return NI_OK;

	}
}

NI_RESULT ZIRE_HAL::CloseConnection() {
	if (!connected_ctrl) {
		return NI_ERROR_NOTCONNECTED;
	}
	else {
        close(sockCTRL);
        connected_ctrl = false;
        CloseSTREAM();
        return NI_OK;
	}
}

NI_RESULT ZIRE_HAL::WriteData(char *value, uint32_t length, uint32_t timeout_ms, uint32_t *written_data) {

	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }

	ret = send(sockCTRL, value, (int)length + 1, 0);

	if (ret < 1) {
		printf("WD: send failed with error: %d\n", ret);
		close(sockCTRL);
		close(sockSTREAM);
		return NI_ERROR_SOCKET;
	}
	else {
	  uint32_t *send_ack = (uint32_t *)malloc(sizeof(uint32_t));
	  ret = recv(sockCTRL, (char*)send_ack, sizeof(uint32_t), 0x8);
	  if (*send_ack = 0x12345678) {
		return NI_OK;
	  }
	}
	return NI_ERROR_SOCKET;
}

NI_RESULT ZIRE_HAL::WriteINTData(int value, uint32_t length, uint32_t timeout_ms, uint32_t *written_data) {
	char buffer[4] = { 0 };
	buffer[0] = value; buffer[1] = value >> 8; buffer[2] = value >> 16; buffer[3] = value >> 24;
	return WriteData(&buffer[0], length - 1, timeout_ms, written_data);
}

NI_RESULT ZIRE_HAL::WriteLONGData(unsigned long long value, uint32_t length, uint32_t timeout_ms, uint32_t *written_data) {
	char buffer[8] = { 0 };
	buffer[0] = value; buffer[1] = value >> 8; buffer[2] = value >> 16; buffer[3] = value >> 24;
	buffer[4] = value >> 32; buffer[5] = value >> 40; buffer[6] = value >> 48; buffer[7] = value >> 56;
	return WriteData(&buffer[0], length - 1, timeout_ms, written_data);
}

NI_RESULT ZIRE_HAL::ReadCharData(char *value, uint32_t length, uint32_t flag, uint32_t timeout_ms) {

	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }

	ret = recv(sockCTRL, value, length, flag);

	if (ret < 1) {
		printf("RCD: send failed with error: %d\n", ret);
		close(sockCTRL);
		return NI_ERROR_SOCKET;
	}

	if (ret = length) {
		return NI_OK;
	}
	else {
		return NI_NO_DATA_AVAILABLE;
	}
}

NI_RESULT ZIRE_HAL::ReadData(uint32_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms) {

	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }

	ret = recv(sockCTRL, (char*)value, length, flag);

	if (ret < 1) {
		printf("RD: send failed with error: %d\n", ret);
		close(sockCTRL);
		return NI_ERROR_SOCKET;
	}

	if (ret = length) {
		return NI_OK;
	}
	else {
		return NI_NO_DATA_AVAILABLE;
	}
}

NI_RESULT ZIRE_HAL::ClearSocket() {
	fd_set readfds;
	FD_ZERO(&readfds);
	FD_SET(sockCTRL, &readfds);

	struct timeval tv;
	tv.tv_sec = 100 / 1000;
	tv.tv_usec = (100 % 1000) * 1000;

	char buffer[1024];
    ssize_t numBytes;

	while (true) {
		ret = select(sockCTRL + 1, &readfds, NULL, NULL, &tv);
		if (ret < -1 ) {
			printf("RS: select failed with error: %d\n", ret);
			close(sockCTRL);
			break;
			return NI_ERROR_SOCKET;
		}

		if (ret == 0) {
			break;
			return NI_TIMEOUT;
		}

		ret = recv(sockCTRL, buffer, sizeof(buffer), 0x8);
        if (ret < -1 ) {
			printf("RS: recv failed with error: %d\n", ret);
			close(sockCTRL);
			break;
			return NI_ERROR_SOCKET;
		}
	}
    return NI_OK;
}

NI_RESULT ZIRE_HAL::ReadSingle(uint32_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms) {

	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }

	ret = recv(sockSTREAM, (char*)value, length, flag);

	if (ret < 1) {
		printf("RD: send failed with error: %d\n", ret);
		close(sockSTREAM);
		return NI_ERROR_SOCKET;
	}

	if (ret = length) {
		return NI_OK;
	}
	else {
		return NI_NO_DATA_AVAILABLE;
	}
}

NI_RESULT ZIRE_HAL::ReadStream(uint64_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms) {
	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }

	fd_set readfds;
	FD_ZERO(&readfds);
	FD_SET(sockSTREAM, &readfds);

	struct timeval tv;
	tv.tv_sec = timeout_ms / 1000;
	tv.tv_usec = (timeout_ms % 1000) * 1000;

	int ret = 0;
	int total_received = 0;

	while (total_received < length) {
		ret = select(sockSTREAM + 1, &readfds, NULL, NULL, &tv);
		if (ret < -1 ) {
			printf("RS: select failed with error: %d\n", ret);
			close(sockCTRL);
			return NI_ERROR_SOCKET;
		}

		if (ret == 0) {
			return NI_TIMEOUT;
		}

		ret = recv(sockSTREAM, ((char*)value) + total_received, length - total_received, flag);
        if (ret < -1 ) {
			printf("RS: recv failed with error: %d\n", ret);
			close(sockCTRL);
			return NI_ERROR_SOCKET;
		}

		if (ret == 0) {
			return NI_SOCKET_NOT_CONNECTED;
		}

		total_received += ret;
	}

	return NI_OK;
}


NI_RESULT ZIRE_HAL::ReadFlowStream(uint64_t *value, uint32_t length, uint32_t flag, uint32_t timeout_ms, int *valid_data) {

	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }
	fd_set set;

	FD_ZERO(&set);				/* clear the set */
	FD_SET(sockSTREAM, &set);	/* add our file descriptor to the set */
	timeout.tv_sec = 1;
	timeout.tv_usec = 0;

	int rv = select(sockSTREAM + 1, &set, NULL, NULL, &timeout);

    if (ret < -1 ) {
		printf("RFS1: send failed with error: %d\n", ret);
		close(sockSTREAM);
		return NI_ERROR_SOCKET;	
	}
	else if (rv == 0)
	{
		return NI_NO_DATA_AVAILABLE;
	}
	else
	{
		uint64_t *_size = (uint64_t *)malloc(sizeof(uint64_t));
		ret = recv(sockSTREAM, (char*)_size, 8, flag);
		uint32_t s_size = (uint32_t)*_size, s_end = (uint64_t)*_size >> 32;

		if (s_end != 0x44454E44) {
			ret = recv(sockSTREAM, (char*)value, s_size, flag);
			if (ret < -1 ) {
				printf("RFS2: send failed with error: %d\n", ret);
				close(sockSTREAM);
				return NI_ERROR_SOCKET;
			}

			*valid_data = ret;
			return NI_OK;
		}
		else {
			ret = recv(sockSTREAM, (char*)value, s_size, flag);
			if (ret < -1 ) {
				printf("RFS3: send failed with error: %d\n", ret);
				close(sockSTREAM);
				return NI_ERROR_SOCKET;
			}

			*valid_data = ret;
			return NI_DATA_END_REQ;
		}
	}
}

NI_RESULT ZIRE_HAL::Enumerate(string board_model, vector<string> devices) {
	if (!connected_ctrl | !connected_stream) { return NI_ERROR_NOTCONNECTED; }
	return NI_OK;
}

NI_RESULT ZIRE_HAL::ConnectSTREAM(string path) {
	if (connected_stream) {
		return NI_ALREADY_CONNECTED;
	}
	else {
		sockaddr_in clientSTREAM;
		clientSTREAM.sin_family = AF_INET;
		clientSTREAM.sin_addr.s_addr = inet_addr(path.c_str());
		clientSTREAM.sin_port = htons(stream_port);
		sockSTREAM = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (sockSTREAM == -1) {
			perror("Socket stream creation error");
			return NI_ERROR_SOCKET;
		}

		if (connect(sockSTREAM, (struct sockaddr*) &clientSTREAM, sizeof(clientSTREAM)) == -1) {
			perror("Connection error");
			close(sockSTREAM);
			return NI_ERROR_SOCKET;
		}

		connected_stream = true;
		return NI_OK;
	}
}

NI_RESULT ZIRE_HAL::CloseSTREAM() {
	if (!connected_stream) {
		return NI_ERROR_NOTCONNECTED;
	}
	else {
		close(sockSTREAM);
		connected_stream = false;
		return NI_OK;
	}
}