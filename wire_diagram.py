import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "docs"

def draw_circuit():
   with schemdraw.Drawing() as d:
      d += elm.Resistor().left().label('R1')
      d += elm.Capacitor().down().label('C1')
      d += elm.Inductor().right().label('L1')
      d += elm.SourceV().up().label('V1')
      d += elm.Ground()

      output_path = OUTPUT_PATH / 'circuit_diagram.png'
      d.save(output_path)
      print(f"Circuit diagram saved to {output_path}")





class ProtoType():

   def __init__(self, parts=None):
      self.name = "Physio Ball"
      self.uprocessor = "ESP8266MOD"
      self.ISM = "2.4GHz"
      self.PA = 26 # dBm
      self.bgn = "802.11b/g/n"
      parts = parts

   def draw(self):
      with schemdraw.Drawing() as d:


         d += elm.Resistor().left().label('R1')
         d += elm.Capacitor().down().label('C1')
         d += elm.Inductor().right().label('L1')
         d += elm.SourceV().up().label('V1')
         d += elm.Ground()

         output_path = OUTPUT_PATH / 'circuit_diagram.png'
         d.save(output_path)
         print(f"Circuit diagram saved to {output_path}")

   class Part():
      def __init__(self, name):
         self.name = name
         self.connections = []

   def circuit(self):
      obj_1 = self.Part("Resistor", [])




def main():
   draw_circuit()
   pP = ProtoType.Part
   parts = [
      pP("Resistor", [1,2]),
      pP("Capacitor", [2,3]),
      pP("Inductor", [3,4]),
      pP("SourceV", [4,5]),
      pP("Ground", [5,1]),
      pP("Microcontroller", [4,6])
   ]

   prototype = ProtoType(parts=parts)



if __name__ == "__main__":
   main()