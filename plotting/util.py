def getData(cfileName):
    """
    Given a name of a *.cfile, this function extracts the interleaved
    Inphase-Quadrature data samples and convert it into a numpy array of complex
    data elements. *.cfile format has interleaved I and Q samples where each sample
    is a float32 type. GNURadio Companion (GRC) scripts output data into a file
    though a file sink block in this format.
    Read more in SDR data types: https://github.com/miek/inspectrum
    """
    # Read the *.cfile which has each element in float32 format.
    data = np.fromfile(cfileName, dtype="float32")
    # print(data[0],data[1],data[2])
    # Take each consecutive interleaved I sample and Q sample to create a single complex element.
    data = data[0::2] + 1j*data[1::2]
    # print("data type=", type(data))
    # Return the complex numpy array.
    return data

## Importing dataset
def loadDataOne(type, payload, freq):
  if type == "udp":
      if payload == 1:
          flag = "udp_all_1"
      else:
          flag = "udp_all_0"
  else:
      if payload == 1:
          flag = "tcp_all_1"
      else:
          flag = "tcp_all_0"

  print(f"Loaded {flag} {freq}.0MHz")
  return getData(f"../dataset/{flag}_freq={freq}.0em_capture.cfile")
