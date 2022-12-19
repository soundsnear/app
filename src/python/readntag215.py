def readNtag215Data(rdr):
  totalString = ""
  for i in range(0,136):
      (someBool, data) = rdr.read(i)
      if i < 6:
        continue
      # print(f'Reading block {i}: ' + str(data))
      startIndex = 1 if i == 6 else 12
      uniqueData = data[startIndex:]
      uniqueData = list(filter(lambda charCode: charCode <= 127 , uniqueData))

      if(all(item == 0 for item in uniqueData)):
        break
      stringValue = "".join(chr(e) for e in uniqueData)
      totalString = totalString + stringValue
      # print("\n" + stringValue + "\n")
  return totalString.strip()