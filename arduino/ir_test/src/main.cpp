// This sketch uses the IrReceiveSampler to receive a signal, and tries to
// decode it as a NEC1 signal

#include <IrReceiverSampler.h>
#include <Nec1Decoder.h>

#define RECEIVE_PIN 8
#define BUFFERSIZE 200U
#define BAUD 115200

IrReceiver *receiver;

void setup() {
    Serial.begin(BAUD);
    receiver = IrReceiverSampler::newIrReceiverSampler(BUFFERSIZE, RECEIVE_PIN);
}

void loop() {
    receiver->receive();

    if (receiver->isEmpty())
        // Serial.println(F("timeout"));
    {}
    else {
        Nec1Decoder decoder(*receiver);
        if (decoder.isValid()){
            const char * strDec = decoder.getDecode();
            Serial.println(strDec);
            // decoder.printDecode(Serial);
        }
        else
            // Serial.println(F("No decode"));
            {}
    }
}
