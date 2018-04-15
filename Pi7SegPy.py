import PiShiftPy as shift

available_chars = {
  0: 0b01111011,
  1: 0b01001000,
  2: 0b01110101,
  3: 0b01011101,
  4: 0b01001110,
  5: 0b00011111,
  6: 0b00111111,
  7: 0b01001001,
  8: 0b01111111,
  9: 0b01001111,
  'A': 0b10001000,
  'b': 0b10000011,
  'C': 0b11000110,
  'c': 0b10100111,
  'd': 0b10100001,
  'E': 0b10000110,
  'F': 0b10001110,
  'H': 0b10001001,
  'h': 0b10001011,
  'L': 0b11000111,
  'n': 0b10101011,
  'I': 0b11111001,
  'O': 0b11000000,
  'o': 0b10100011,
  'P': 0b10001100,
  'S': 0b10010010,
  ' ': 0b11111111
}

data = 18
clock = 23
latch = 24
chain = 2
displays = 1
common_cathode = False

def init(data_pin=18, clock_pin=23, latch_pin=24, registers=1, no_of_displays=1, common_cathode_type=False):
  global data, clock, latch, chain, common_cathode, displays
  data = data_pin
  clock = clock_pin
  latch = latch_pin
  chain = registers
  common_cathode = common_cathode_type
  displays = no_of_displays
  setup()


def setup():
  if common_cathode:
    for key in available_chars:
      available_chars[key] = ~available_chars[key]
  shift.init(data, clock, latch, chain)


def with_dot(value):
  return value & ~(1 << 7)

def show(values, dots=[]):
  #values.reverse()
  length = len(values)
  numberOfZeroes = chain - length
  print("number of zeros")
  print(numberOfZeroes)
  if length > displays*chain:
    raise ValueError("More Characters than available on displays")
  else:
    #need to first send in zeroes to control the current going through the system
    for i in range(numberOfZeroes):
      try:
        char = 0b01111011
        if i+1 in dots:
            char = with_dot(0b01111011)
        shift.write(char)
      except KeyError:
        raise ValueError("The character cannot be printed on a 7 segment display")
    #after sending in zeros, we send in the actual values
    for i in range(length):
      try:
        char = available_chars[values[i]]
        if i+1 in dots:
          char = with_dot(char)
        #print(char << 8 | 1 << i)
        print(char)
        shift.write(char)
      except KeyError:
        raise ValueError("The character cannot be printed on a 7 segment display")
