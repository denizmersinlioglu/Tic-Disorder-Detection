#include "Arduino.h"
#include "MPU9250.h"
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// BluetoothSerial SerialBT;
// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire, 0x68);
int status;

void setup()
{
  Serial.begin(19200);
  // SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  status = IMU.begin();

  if (status < 0)
  {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while (1)
    {
    }
  }
}

void loop()
{

  // read the sensor
  IMU.readSensor();
  // Serial.print(SerialBT.available());

  // Serial.print("Looped");
  Serial.print(IMU.getAccelX_mss(), 4);
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss(), 4);
  Serial.print("\t");
  Serial.print(IMU.getAccelZ_mss(), 4);
  Serial.print("\t");
  Serial.print(IMU.getGyroX_rads(), 4);
  Serial.print("\t");
  Serial.print(IMU.getGyroY_rads(), 4);
  Serial.print("\t");
  Serial.print(IMU.getGyroZ_rads(), 4);
  Serial.print("\n");

  delay(38);
}

// void loop()
// {
//   // read the sensor
//   IMU.readSensor();

//   if (Serial.available())
//   {
//     SerialBT.print(IMU.getAccelX_mss(), 6);
//     SerialBT.print("\t");
//     SerialBT.print(IMU.getAccelY_mss(), 6);
//     SerialBT.print("\t");
//     SerialBT.print(IMU.getAccelZ_mss(), 6);
//     SerialBT.print("\t");
//     SerialBT.print(IMU.getGyroX_rads(), 6);
//     SerialBT.print("\t");
//     SerialBT.print(IMU.getGyroY_rads(), 6);
//     SerialBT.print("\t");
//     SerialBT.print(IMU.getGyroZ_rads(), 6);
//     SerialBT.print("\n");
//   }

//   // Serial.print(IMU.getMagX_uT(), 6);
//   // Serial.print("\t");
//   // Serial.print(IMU.getMagY_uT(), 6);
//   // Serial.print("\t");
//   // Serial.print(IMU.getMagZ_uT(), 6);
//   // Serial.print("\t");
//   // Serial.println(IMU.getTemperature_C(), 6);
//   delay(10);
// }