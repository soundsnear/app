from pirc522 import RFID
rdr = RFID()

def readData(rdr):
  totalString = ""
  for i in range(0,136):
      (someBool, data) = rdr.read(i)
      if i < 6:
        continue
      print(f'Reading block {i}: ' + str(data))
      startIndex = 1 if i == 6 else 12
      uniqueData = data[startIndex:]
      uniqueData = list(filter(lambda charCode: charCode <= 127 , uniqueData))

      if(all(item == 0 for item in uniqueData)):
        break
      stringValue = "".join(chr(e) for e in uniqueData)
      totalString = totalString + stringValue
      print("\n" + stringValue + "\n")
  return totalString
    

while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):
          data = readData(rdr)
          print(f"read: {data}")
          break
          # Always stop crypto1 when done working
          rdr.stop_crypto()
# Calls GPIO cleanup
rdr.cleanup()