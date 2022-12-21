def readNtag215Data(rdr):
  totalString = ""
  for i in range(0,136):
      (someBool, data) = rdr.read(i)
      if i < 6:
        continue
      # print(f'Reading block {i}: ' + str(data))
      startIndex = 1 if i == 6 else 12
      uniqueData = data[startIndex:]

      if(all(item == 0 for item in uniqueData)):
        break
    
      uniqueData = list(filter(lambda charCode: charCode > 0 and charCode <= 127, uniqueData))
      stringValue = "".join(chr(e) for e in uniqueData)
      totalString = totalString + stringValue
      # print("\n" + repr(stringValue) + "\n")
      should_be_length = 16 - startIndex
      is_at_end = len(uniqueData) < should_be_length
      # sometimes the card has old data in later blocks. This prevents reading and appending that.
      # TODO: read the spec and see if there are more details instructions on data length or something like that instead of this hack
      if is_at_end:
          break
  return totalString.strip()
